import pytest

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

import bike_inventory


@pytest.fixture
def tracer():
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__)
    return tracer


def test_manufacturer_url_update():
    tracer = trace.get_tracer(__name__)
    bikes = bike_inventory.get(tracer)
    assert bikes[0]['url'] != 'unknown'
