from yattag import Doc


def get_html_table(doc: Doc, headers: list, bikes: list) -> Doc:
    """Generates a table of bikes

    Args:
        doc (Doc): HTML doc
        headers (list): a list of headers to populate a table
        bikes (list): a list of bikes as table rows

    Returns:
        Doc: HTML doc with table
    """

    def add_headers(doc, headers):
        with doc.tag('tr'):
            for header in headers:
                doc.line('th', header)

    def add_row(doc, row):
        with doc.tag('tr'):
            for _, value in row.items():
                if isinstance(value, list) is False:
                    with doc.tag('td'):
                        doc.text(value)

    with doc.tag('table', id='bikes_inventory'):
        with doc.tag('tbody'):
            add_headers(doc, headers)

            for bike in bikes:
                add_row(doc, bike)

    return doc


def get_html_header(doc: Doc):
    with doc.tag('head'):
        doc.stag('link', rel='stylesheet', href='css/styles.css')

    return doc
