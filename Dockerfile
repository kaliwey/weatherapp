FROM python:3.8-alpine3.14

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir pipenv && \
    pipenv install --clear

RUN chmod a+rwx -R /app