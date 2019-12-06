FROM python:3.7-alpine

WORKDIR /app
ADD . .

RUN pip install pipenv gunicorn && \
    pipenv install --system --deploy --ignore-pipfile && \
