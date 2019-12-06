FROM python:3.7-alpine

WORKDIR /app
ADD . .

RUN pip install pipenv gunicorn && \
    pipenv install --system --deploy --ignore-pipfile

CMD ["/usr/local/bin/gunicorn", "-c", "gunicorn.py", "wsgi:app"]
