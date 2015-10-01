# -*- encoding: utf-8 -*-
import datetime
import gzip
import os
import re
import traceback
from xml.dom import minidom
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree


class Bootstrapper(object):

    ### CLASS VARIABLES ###

    date_regex = re.compile('^(\d{4})-(\d{2})-(\d{2})$')
    date_no_dashes_regex = re.compile('^(\d{4})(\d{2})(\d{2})$')
    year_regex = re.compile('^\d\d\d\d$')

    data_directory = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
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
    def element_to_datetime(element):
        if element is None:
            return None
        date_string = element.text.strip()
        # empty string
        if not date_string:
            return None
        # yyyy-mm-dd
        match = Bootstrapper.date_regex.match(date_string)
        if match:
            year, month, day = match.groups()
            return Bootstrapper.validate_release_date(year, month, day)
        # yyyymmdd
        match = Bootstrapper.date_no_dashes_regex.match(date_string)
        if match:
            year, month, day = match.groups()
            return Bootstrapper.validate_release_date(year, month, day)
        # yyyy
        match = Bootstrapper.year_regex.match(date_string)
        if match:
            year, month, day = match.group(), '1', '1'
            return Bootstrapper.validate_release_date(year, month, day)
        # other: "?", "????", "None", "Unknown"
        return None

    @staticmethod
    def element_to_integer(element):
        if element is not None:
            return int(element.text)
        return None

    @staticmethod
    def element_to_string(element):
        if element is not None:
            return element.text or None
        return None

    @staticmethod
    def element_to_strings(element):
        if element is not None and len(element):
            return [_.text for _ in element]
        return None

    @staticmethod
    def get_iterator(tag):
        choices = {
            'artist': Bootstrapper.artists_xml_path,
            'label': Bootstrapper.labels_xml_path,
            'master': Bootstrapper.masters_xml_path,
            'release': Bootstrapper.releases_xml_path,
            }
        file_pointer = gzip.GzipFile(choices[tag], 'r')
        iterator = Bootstrapper.iterparse(file_pointer, tag)
        iterator = Bootstrapper.clean_elements(iterator)
        return iterator

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
    def prettify(element):
        string = ElementTree.tostring(element, 'utf-8')
        reparsed = minidom.parseString(string)
        return reparsed.toprettyxml(indent='    ')

    @staticmethod
    def validate_release_date(year, month, day):
        try:
            year = int(year)
            if month.isdigit():
                month = int(month)
            if month < 1:
                month = 1
            if day.isdigit():
                day = int(day)
            if day < 1:
                day = 1
            date = datetime.datetime(year, month, 1, 0, 0)
            day_offset = day - 1
            date = date + datetime.timedelta(days=day_offset)
        except ValueError:
            traceback.print_exc()
            print('BAD DATE:', year, month, day)
            date = None
        return date