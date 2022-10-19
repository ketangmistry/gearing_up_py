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

    with doc.tag('table', id='bikes_inventory'):
        with doc.tag('tbody'):
            add_headers(doc, headers)

    return doc
