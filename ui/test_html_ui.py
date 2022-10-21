import pytest

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

from yattag import Doc

import api.bike_inventory as bike_inventory

import html_ui


@pytest.fixture
def tracer():
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    return tracer


TABLE_HEADERS = [
    'manufacturer',
    'model',
    'url'
]


def test_table_headers():
    tracer = trace.get_tracer(__name__)
    doc, tag, text, line = Doc().ttl()
    bikes = bike_inventory.get(tracer)
    doc = html_ui.get_html_table(doc, TABLE_HEADERS, bikes)
    assert doc.getvalue().index('<table id="bikes_inventory">') == 0
