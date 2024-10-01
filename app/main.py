import socket
import logging
import sys
import os
import string
import secrets
from flask import Flask, jsonify, request, session


def generate_secret_key(length=38):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", default=generate_secret_key())
app.config['SESSION_COOKIE_NAME'] = os.environ.get(
    "SESSION_COOKIE_NAME", default=f"session-flask-hello-world-{generate_secret_key(length=4)}")

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


@app.route('/health')
def health():
    return jsonify({
        "status": "OK"
    }), 200


@app.route('/')
def hello_world():

    hostname = socket.gethostname()

    if "counter" not in session:
        session["counter"] = 0

    if "hostnames" not in session:
        session["hostnames"] = {}

    if socket.gethostname() not in session["hostnames"]:
        session["hostnames"][hostname] = 0

    session["hostnames"][hostname] += 1
    session["counter"] += 1

    debug_msg = {
        "counter": session["counter"],
        "host": socket.getfqdn(),
        "hostnames": session["hostnames"],
        "request": {
            "method": request.method,
            "url": request.url,
            "base_url": request.base_url,
            "url_root": request.url_root,
            "url_rule": str(request.url_rule),
            "host_url": request.host_url,
            "host": request.host,
            "script_root": request.script_root,
            "path": request.path,
            "full_path": request.full_path,
            "args": request.args,
        },
    }

    app.logger.debug(debug_msg)

    return jsonify(debug_msg)
