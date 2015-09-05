from __future__ import print_function
import gzip
import mongoengine
import traceback
from abjad.tools import systemtools
from discograph.bootstrap import Bootstrap
from discograph.models.LabelReference import LabelReference
from discograph.models.Model import Model


class Label(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(primary_key=True)
    name = mongoengine.StringField(required=True, unique=True)
    parent_label = mongoengine.EmbeddedDocumentField(LabelReference)
    sublabels = mongoengine.EmbeddedDocumentListField('LabelReference')

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            'discogs_id',
            'name',
            '$name',
            ],
        }

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_collection()
        # Pass one.
        labels_xml_path = Bootstrap.labels_xml_path
        with gzip.GzipFile(labels_xml_path, 'r') as file_pointer:
            iterator = Bootstrap.iterparse(file_pointer, 'label')
            iterator = Bootstrap.clean_elements(iterator)
            for i, element in enumerate(iterator):
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        document = cls.from_element(element)
                        document.save()
                        message = u'{} (Pass 1) {} [{}]: {}'.format(
                            cls.__name__.upper(),
                            document.discogs_id,
                            timer.elapsed_time,
                            document.name,
                            )
                        print(message)
                except mongoengine.errors.ValidationError:
                    traceback.print_exc()
        # Pass two.
        count = cls.objects.count()
        for index in range(count):
            document = cls.objects.no_cache()[index]
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references()
                if changed:
                    document.save()
                    message = u'{} (Pass 2) {} [{}]: {}'.format(
                        cls.__name__.upper(),
                        document.discogs_id,
                        timer.elapsed_time,
                        document.name,
                        )
                    print(message)

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        document = cls(**data)
        return document

    def resolve_references(self):
        changed = False
        for label_reference in self.sublabels:
            query = type(self).objects(name=label_reference.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if not len(found):
                continue
            label_reference.discogs_id = found[0].discogs_id
            changed = True
        if self.parent_label:
            query = type(self).objects(name=self.parent_label.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found):
                self.parent_label.discogs_id = found[0].discogs_id
                changed = True
        return changed


Label._tags_to_fields_mapping = {
    'id': ('discogs_id', Bootstrap.element_to_integer),
    'name': ('name', Bootstrap.element_to_string),
    'sublabels': ('sublabels', LabelReference.from_sublabels),
    'parentLabel': ('parent_label', LabelReference.from_parent_label),
    }