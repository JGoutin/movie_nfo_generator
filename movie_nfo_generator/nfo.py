"""NFO file utilities"""
from lxml.etree import Element, SubElement, ElementTree
from os.path import join


def write_nfo(root_name, nfo_fields, media_filename, link="", filename=None):
    """
    Write the NFO file

    Args:
        root_name (str): NFO root name.
        nfo_fields (dict): Fields.
        media_filename (str): Media file name.
        link (str): Scrapper URL link.
        filename (str): NFO file name.
    """
    nfo_root = Element(root_name)

    for field_name, values in nfo_fields.items():
        if not values:
            continue
        if not isinstance(values, list):
            values = [values]
        for value in values:
            SubElement(nfo_root, field_name).text = f"{value}"

    if not filename:
        filename = f"{media_filename}.nfo"
    else:
        filename = join(media_filename, filename)

    ElementTree(nfo_root).write(
        filename, encoding="utf-8", xml_declaration=True, pretty_print=True
    )

    if link:
        with open(filename, "at") as nfo_file:
            nfo_file.write(link)
