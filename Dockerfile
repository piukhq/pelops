FROM python:3.6

ADD . /app

RUN pip install uwsgi && pip install -r /app/requirements.txt

