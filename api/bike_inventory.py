from opentelemetry import trace
from opentelemetry.sdk.trace import Tracer

from data.bikes import get_yaml_object_from_file

from services.bike_index_api import get_manufacturer_by_name

BIKE_INVENTORY_FILE = 'bikes.yaml'


def get(tracer: Tracer) -> list:
    """Get a list of bikes from file with the manufacturer URL enriched

    Returns:
        list: list of bikes with full details
    """
    yaml_file = get_yaml_object_from_file(BIKE_INVENTORY_FILE)

    def updater(bike_wrapper):

        manu = bike_wrapper['bike']['manufacturer']

        with tracer.start_as_current_span(
            'get_' + str(manu) + '_data', kind=trace.SpanKind.CLIENT
        ) as span:
            status_code, bike_index_res = get_manufacturer_by_name(
                manu
            )

            span.set_attributes(
                {'manufacturer': manu}
            )

            if status_code >= 400:
                span.set_status(trace.Status(trace.StatusCode.ERROR))
                url = 'not found!'
            else:
                span.set_status(trace.Status(trace.StatusCode.OK))
                url = bike_index_res['manufacturer']['company_url']

            bike_wrapper['bike']['url'] = url

        return bike_wrapper['bike']

    updates_bikes = [
        updater(bike_wrapper) for bike_wrapper in yaml_file['bikes']
    ]

    return updates_bikes
