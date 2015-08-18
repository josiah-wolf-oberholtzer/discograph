import os
from xml.etree import ElementTree


data_directory = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'data',
    )

artists_xml_path = os.path.join(
    data_directory,
    'discogs_20150810_artists.xml.gz',
    )

labels_xml_path = os.path.join(
    data_directory,
    'discogs_20150810_labels.xml.gz',
    )

masters_xml_path = os.path.join(
    data_directory,
    'discogs_20150810_masters.xml.gz',
    )

releases_xml_path = os.path.join(
    data_directory,
    'discogs_20150810_releases.xml.gz',
    )


def clean_element(element):
    image_tags = element.findall('images')
    if image_tags:
        element.remove(*image_tags)
    url_tags = element.findall('urls')
    if url_tags:
        element.remove(*url_tags)
    return element


def iterparse(source, tag):
    context = ElementTree.iterparse(
        source,
        events=('start', 'end',),
        )
    context = iter(context)
    _, root = next(context)
    depth = 0
    for event, element in context:
        if element.tag == tag:
            if event == 'start':
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    yield clean_element(element)
                    root.clear()