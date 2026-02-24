'''
   Default test for Boilerplate App
'''
import random
import string
from webapp.app import app

C = app.test_client()


# configure the SQLite database, relative to the app instance folder
# initialize the app with the extension
# db.init_app(app)


def __random_string(length=32):
    '''Generates random string'''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# def test_request_example(client=C):
#    '''Checks basic field in response data'''
#    test_json_returned()
#    response = client.get("/basic")
#    assert b"basic" in response.data
#
# def test_request_basic(client=C):
#    '''Checks json formatting of basic'''
#    test_json_returned()
#    response = client.get("/basic")
#    assert response.json["items"]
#
#
# def test_request_json(client=C):
#    '''Checks json formatting of basic'''
#    test_json_returned()
#    response = client.get("/basic")
#    assert response.json["items"]
#
#

def test_json_returned(client=C):
    '''Sends random basic data and ensures it is returned'''
    rnd_str = __random_string()
    response = client.post("/basic",
                           json={
                               "mandatory": rnd_str,
                               "optional": "dave"})
    assert response.json["mandatory"] == rnd_str
    response = client.get("/basic")
    assert rnd_str in str(response.data)
