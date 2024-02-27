FROM ghcr.io/binkhq/python:3.12
ARG PIP_INDEX_URL
ARG APP_NAME
ARG APP_VERSION
WORKDIR /app
RUN pip install --no-cache ${APP_NAME}==$(echo ${APP_VERSION} | cut -c 2-)
ADD wsgi.py .

CMD [ "gunicorn", "--error-logfile=-", "--access-logfile=-", \
    "--logger-class=pelops.reporting.CustomGunicornLogger", \
    "--bind=0.0.0.0:9000", "wsgi:app" ]
