FROM python:3.6

WORKDIR /app
ADD . .

RUN pip install uwsgi && pip install -r /app/requirements.txt