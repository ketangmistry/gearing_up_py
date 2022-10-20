#!/usr/bin/env python3
import os

import flask
from flask import Flask, send_from_directory
from flask_cors import CORS

from yattag import Doc

from api.bike_inventory import get as bike_index_get
from ui.html_ui import get_html_table, get_html_header

APP_NAME = 'gearing_up_py'


def create_app(config=None):
    """_summary_

    Args:
        config (_type_, optional): Everything to create a Flask app.
        Defaults to None.

    Returns:
        _type_: the Flask app
    """
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    CORS(app)

    @app.route('/css/styles.css', methods=['GET'])
    def styles():
        return send_from_directory('css', 'styles.css')

    @app.route('/inventory', methods=['GET'])
    def root():
        doc, tag, text, line = Doc().ttl()
        doc = get_html_header(doc)

        status = 200
        TABLE_HEADERS = [
            'manufacturer',
            'model',
            'url'
        ]
        bikes = bike_index_get()
        doc = get_html_table(doc, TABLE_HEADERS, bikes)

        res = flask.Response(doc.getvalue(), status=status)
        res.headers['app'] = APP_NAME

        return res

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
