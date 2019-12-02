FROM python:3-alpine

RUN apk --no-cache --update add build-base dumb-init

COPY ./requirements.txt /requirements.txt

RUN pip install -U -r requirements.txt

ADD app /app

WORKDIR /app

ENV SECRET_KEY=cne287fg8237hc38igochh98cy^TR^&%R&T*&G

ENV SESSION_COOKIE_NAME=session-flask-hello-world

EXPOSE 5000

ENTRYPOINT ["/usr/bin/dumb-init", "--", "gunicorn", "--bind=0.0.0.0:5000", "--workers=1", "--worker-class=gthread", "--preload", "main:app"]

CMD [ "--log-level=info" ]
