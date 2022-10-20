#!/usr/bin/env python3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.sdk.resources import Resource

import os

import flask
from flask import Flask, send_from_directory
from flask_cors import CORS

from yattag import Doc

from api.bike_inventory import get as bike_index_get
from ui.html_ui import get_html_table, get_html_header

APP_NAME = 'gearing_up_py'

# set the correct naming in otel
resource = Resource.create({"service.name": APP_NAME})

# getting the otel tracer setup asap
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# similarly getting the otel meter setup asap
metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)


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

        with tracer.start_as_current_span(
            'call_bike_index_api'
        ) as parent_span:
            parent_span.set_attribute(SpanAttributes.HTTP_METHOD, 'GET')
            bikes = bike_index_get(tracer)
            with tracer.start_as_current_span('render_inventory'):
                doc = get_html_table(doc, TABLE_HEADERS, bikes)

        res = flask.Response(doc.getvalue(), status=status)
        res.headers['app'] = APP_NAME

        return res

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
