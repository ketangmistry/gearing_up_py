from yattag import Doc


def get_html_table(doc: Doc, headers: list, bikes: list) -> Doc:

    def add_headers(doc, headers):
        with doc.tag('tr'):
            for header in headers:
                doc.line('th', header)

    with doc.tag('table', id='bikes_inventory'):
        with doc.tag('tbody'):
            add_headers(doc, headers)

    return doc
