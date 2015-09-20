# -*- encoding: utf-8 -*-
from __future__ import print_function
import gzip
import mongoengine
import os
import random
import traceback
from abjad.tools import systemtools
from discograph import Bootstrapper
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
            '#name',
            '$name',
            'discogs_id',
            'name',
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
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        # Pass one.
        labels_xml_path = Bootstrapper.labels_xml_path
        with gzip.GzipFile(labels_xml_path, 'r') as file_pointer:
            iterator = Bootstrapper.iterparse(file_pointer, 'label')
            iterator = Bootstrapper.clean_elements(iterator)
            for i, element in enumerate(iterator):
                try:
                    with systemtools.Timer(verbose=False) as timer:
                        document = cls.from_element(element)
                        cls.objects.insert(document, load_bulk=False)
                        #document.save()
                        #document.save(force_insert=True)
                    message = u'{} (Pass 1) {} [{}]: {}'.format(
                        cls.__name__.upper(),
                        document.discogs_id,
                        timer.elapsed_time,
                        document.name,
                        )
                    print(message)
                except mongoengine.errors.ValidationError:
                    traceback.print_exc()

    @classmethod
    def bootstrap_pass_two(cls):
        # Pass two.
        cls.ensure_indexes()
        query = cls.objects().no_cache().timeout(False)
        for i, document in enumerate(query):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references_one_query()
            if not changed:
                message = u'{} [SKIPPED] (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                    cls.__name__.upper(),
                    i,
                    document.discogs_id,
                    timer.elapsed_time,
                    document.name,
                    )
                print(message)
                continue
            document.save()
            #assert not document.resolve_references()
            message = u'{} (Pass 2) (idx:{}) (id:{}) [{:.8f}]: {}'.format(
                cls.__name__.upper(),
                i,
                document.discogs_id,
                timer.elapsed_time,
                document.name,
                )
            print(message)

    @classmethod
    def dump_to_csv(cls, file_path=None):
        import discograph
        if file_path is None:
            file_path = os.path.join(
                discograph.__path__[0],
                'data',
                '{}.csv'.format(cls.__name__.lower()),
                )
        query = cls.objects().no_cache().timeout(False)
        count = query.count()
        file_pointer = open(file_path, 'w')
        progress_indicator = systemtools.ProgressIndicator(
            message='Processing', total=count)
        with file_pointer, progress_indicator:
            line = 'id;name\n'
            file_pointer.write(line)
            for document in query:
                discogs_id = document.discogs_id
                name = document.name
                if discogs_id and name:
                    name = name.replace('"', r'\"')
                    line = '{};"{}"\n'.format(discogs_id, name)
                    file_pointer.write(line)
                progress_indicator.advance()

    @staticmethod
    def dump_to_sqlite():
        import discograph
        discograph.SQLLabel.drop_table(fail_silently=True)
        discograph.SQLLabel.create_table()
        query = discograph.Label.objects().no_cache().timeout(False)
        query = query.only('discogs_id', 'name')
        count = query.count()
        rows = []
        for i, mongo_document in enumerate(query, 1):
            if mongo_document.discogs_id and mongo_document.name:
                rows.append(dict(
                    id=mongo_document.discogs_id,
                    name=mongo_document.name,
                    random=random.random(),
                    ))
            if len(rows) == 100:
                discograph.SQLLabel.insert_many(rows).execute()
                rows = []
                print('Processing... {} of {} [{:.3f}%]'.format(
                    i, count, (float(i) / count) * 100))
        if rows:
            discograph.SQLLabel.insert_many(rows).execute()
            print('Processing... {} of {} [{:.3f}%]'.format(
                i, count, (float(i) / count) * 100))

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        document = cls(**data)
        return document

    @classmethod
    def get_label_corpus(cls):
        query = cls.objects.only('discogs_id', 'name').all().as_pymongo()
        labels = {}
        for item in query:
            if item['name'] in labels:
                print(item['name'])
            labels[item['name']] = item['_id']
        return labels

    def resolve_references(self):
        changed = False
        for reference in self.sublabels:
            query = type(self).objects(name=reference.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found) and found[0].discogs_id != reference.discogs_id:
                reference.discogs_id = found[0].discogs_id
                changed = True
            elif not len(found) and reference.discogs_id:
                reference.discogs_id = None
                changed = True
        if self.parent_label:
            query = type(self).objects(name=self.parent_label.name)
            query = query.only('discogs_id', 'name')
            found = list(query)
            if len(found) and found[0].discogs_id != self.parent_label.discogs_id:
                self.parent_label.discogs_id = found[0].discogs_id
                changed = True
        return changed


Label._tags_to_fields_mapping = {
    'id': ('discogs_id', Bootstrapper.element_to_integer),
    'name': ('name', Bootstrapper.element_to_string),
    'sublabels': ('sublabels', LabelReference.from_sublabels),
    'parentLabel': ('parent_label', LabelReference.from_parent_label),
    }