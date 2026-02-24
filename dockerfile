FROM python
RUN adduser app
COPY requirements.txt /home/app
RUN pip install -r /home/app/requirements.txt
RUN echo "#!/bin/bash">>/bin/entrypoint.sh
EXPOSE 5000
RUN echo gunicorn --certfile=/home/app/askmartyn.com.crt.pem --keyfile=/home/app/askmartyn.com.key.pem --bind 0.0.0.0:5000 webapp.app:app>>/bin/entrypoint.sh
COPY . /home/app
RUN chmod +x /bin/entrypoint.sh
RUN pip install /home/app 
CMD ["/bin/entrypoint.sh"]
