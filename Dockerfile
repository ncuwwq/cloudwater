FROM python:3
COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
WORKDIR .
EXPOSE 8080
CMD gunicorn --workers 3 -b 0.0.0.0:8080 --user root --worker-class gevent manage:app
CMD gunicorn --workers 3 --user root --worker-class gevent MQTTClient:app