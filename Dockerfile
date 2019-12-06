FROM python:3.6

WORKDIR /app
ADD . .

RUN pip install pipenv gunicorn && \
    pipenv install --system --deploy --ignore-pipfile && \

