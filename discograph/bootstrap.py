import gzip
import os
import six
import textwrap
from xml.dom import minidom
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


def clean_elements(elements):
    for element in elements:
        image_tags = element.findall('images')
        if image_tags:
            element.remove(*image_tags)
        url_tags = element.findall('urls')
        if url_tags:
            element.remove(*url_tags)
        yield element


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


def get_iterator(tag):
    choices = {
        'artist': artists_xml_path,
        'label': labels_xml_path,
        'master': masters_xml_path,
        'release': releases_xml_path,
        }
    file_pointer = gzip.GzipFile(choices[tag], 'r')
    iterator = iterparse(file_pointer, tag)
    iterator = clean_elements(iterator)
    return iterator


def prettify(element):
    string = ElementTree.tostring(element, 'utf-8')
    reparsed = minidom.parseString(string)
    return reparsed.toprettyxml(indent='    ')


def normalize(string, indent=None):
    string = string.replace('\t', '    ')
    lines = string.split('\n')
    while lines and (not lines[0] or lines[0].isspace()):
        lines.pop(0)
    while lines and (not lines[-1] or lines[-1].isspace()):
        lines.pop()
    for i, line in enumerate(lines):
        lines[i] = line.rstrip()
    string = '\n'.join(lines)
    string = textwrap.dedent(string)
    if indent:
        if not isinstance(indent, six.string_types):
            indent = ' ' * abs(int(indent))
        lines = string.split('\n')
        for i, line in enumerate(lines):
            if line:
                lines[i] = '{}{}'.format(indent, line)
        string = '\n'.join(lines)
    return string