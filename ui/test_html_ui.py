from yattag import Doc

import api.bike_inventory as bike_inventory

import html_ui


TABLE_HEADERS = [
    'manufacturer',
    'model',
    'url'
]


def test_table_headers():
    doc, tag, text, line = Doc().ttl()
    bikes = bike_inventory.get()
    doc = html_ui.get_html_table(doc, TABLE_HEADERS, bikes)
    assert doc.getvalue().index('<table id="bikes_inventory">') == 0
