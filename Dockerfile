FROM python:3
COPY ./requirements.txt /tmp/
ADD MQTTClient.py /
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
WORKDIR .
EXPOSE 8080
CMD gunicorn --workers 3 -b 0.0.0.0:8080  manage:app && python ./MQTTClient.py