import os
import gzip
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


def iterparse(xml_path, tag):
    gzip_file = gzip.GzipFile(xml_path, 'r')
    context = ElementTree.iterparse(gzip_file, events=('start', 'end',))
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
                    yield element
                    root.clear()


def clean_element(element):
    image_tags = element.findall('images')
    element.remove(*image_tags)