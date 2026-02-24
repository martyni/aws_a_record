'''Basic flask app'''
from os import environ, path
from flask import Flask, request, jsonify
import webapp
from webapp.models import Basic, db

conf_file = environ.get(
    'WEBAPP_CONF') or f'{path.dirname(webapp.__file__)}/config.py'
print(conf_file)
GOOD_DATA = {
    "mandatory": "<mandatory>",
    "optional": "<optional(optional)>",
}


def create_app(config_filename):
    '''App factory for Webapp'''
    new_app = Flask(__name__)
    new_app.config.from_pyfile(config_filename, silent=False)
    db.init_app(new_app)
    print(new_app.config)
    with new_app.app_context():
        db.create_all()

    # from yourapplication.views.admin import admin
    # from yourapplication.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)

    @new_app.route('/basic', methods=['GET'])
    def get_paginated_items():
        '''Return paginated items based on page and per_page values'''
        page = int(request.args.get('page')) if request.args.get('page') else 1
        per_page = int(request.args.get('per_page')
                       ) if request.args.get('per_page') else 5
        items = Basic.query.order_by(Basic.date.desc()) \
            .paginate(page=page,
                      per_page=per_page,
                      error_out=False)
        return jsonify({
            "items": [item.to_dict() for item in items.items],
            "total": items.total,
            "page": items.page,
            "pages": items.pages,
            "next_page": f'/basic?page={ page + 1 }&per_page={ per_page }'
        }), 200

    @new_app.route('/basic', methods=['POST'])
    def receive_message():
        '''URL for recieving items'''
        data = request.get_json()
        print(data)

        if not data or 'mandatory' not in data:
            return jsonify({
                'error': 'Invalid input',
                'recieved': f'{data}',
                'expected': f'{GOOD_DATA}'}), 400

        new_item = Basic(
            mandatory=data['mandatory'],
            optional=data.get('optional'))
        db.session.add(new_item)
        db.session.commit()

        return jsonify(new_item.to_dict()), 201

    @new_app.route('/')
    def root():
        '''App index'''
        return get_paginated_items()
    return new_app


app = create_app(conf_file)

if __name__ == "__main__":
    app.run()
    #app.run(debug=True) #For debugging local dev issues
