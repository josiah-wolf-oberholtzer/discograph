import gzip
import os
from xml.dom import minidom
from xml.etree import ElementTree


class Bootstrap(object):

    ### CLASS VARIABLES ###

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

    ### PUBLIC METHODS ###

    @staticmethod
    def clean_elements(elements):
        for element in elements:
            image_tags = element.findall('images')
            if image_tags:
                element.remove(*image_tags)
            url_tags = element.findall('urls')
            if url_tags:
                element.remove(*url_tags)
            yield element

    @staticmethod
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
                        yield element
                        root.clear()

    @staticmethod
    def get_iterator(tag):
        choices = {
            'artist': Bootstrap.artists_xml_path,
            'label': Bootstrap.labels_xml_path,
            'master': Bootstrap.masters_xml_path,
            'release': Bootstrap.releases_xml_path,
            }
        file_pointer = gzip.GzipFile(choices[tag], 'r')
        iterator = Bootstrap.iterparse(file_pointer, tag)
        iterator = Bootstrap.clean_elements(iterator)
        return iterator

    @staticmethod
    def prettify(element):
        string = ElementTree.tostring(element, 'utf-8')
        reparsed = minidom.parseString(string)
        return reparsed.toprettyxml(indent='    ')