#!/usr/bin/env python3
import os

import flask
from flask import Flask, request
from flask_cors import CORS
from logzero import logger


def create_app(config=None):
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    CORS(app)

    @app.route('/', methods=['GET'])
    def root():
        req_content_type = request.headers.get('Content-Type')

        if req_content_type != 'application/json':
            status = 400
            text = 'bad request'
            logger.error('bad request because content type is "%s"',
                         req_content_type)
        else:
            status = 200
            text = 'all good'

        res = flask.Response(text, status=status)
        res.headers['app'] = __name__

        return res

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
