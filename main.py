#!/usr/bin/env python3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from prometheus_client import start_http_server

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricReader

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
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer('opentelemetry.instrumentation.flask')

# start Prometheus client
start_http_server(port=8000, addr="localhost")

# similarly getting the otel meter setup asap
metric_reader = PrometheusMetricReader()
provider = MeterProvider(metric_readers=[metric_reader], resource=resource)
metrics.set_meter_provider(provider)
meter = metrics.get_meter('opentelemetry.instrumentation.flask')

# define metrics to collect
inventory_request_counter = meter.create_counter(
    "inventory_request",
    unit="num",
    description="Number of requests to inventory API route"
)


def create_app(config=None):
    """Create a Flask web app

    Args:
        config (_type_, optional): Everything to create a Flask app.
        Defaults to None.

    Returns:
        _type_: the Flask app object
    """
    app = Flask(__name__)

    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    CORS(app)

    @app.route('/css/styles.css', methods=['GET'])
    def styles():
        return send_from_directory('css', 'styles.css')

    @app.route('/inventory', methods=['GET'])
    def inventory():
        inventory_request_counter.add(1)

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
    port = int(os.environ.get("PORT", 8080))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
