import socket
import logging
import sys
from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "cne287fg8237hc38igochh98cy^TR^&%R&T*&G"

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)


@app.route('/health')
def health():
    return "OK", 200


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
        "request": str(request),
    }

    app.logger.debug(debug_msg)

    return jsonify(debug_msg)
