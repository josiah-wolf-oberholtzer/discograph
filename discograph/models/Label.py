from __future__ import print_function
import gzip
import mongoengine
from discograph.models.Model import Model


class Label(Model, mongoengine.Document):

    ### MONGOENGINE FIELDS ###

    discogs_id = mongoengine.IntField(unique=True, null=True, sparse=True)
    name = mongoengine.StringField(required=True, unique=True)
    parent_label = mongoengine.ReferenceField('Label')
    sublabels = mongoengine.ListField(mongoengine.ReferenceField('Label'))
    has_been_scraped = mongoengine.BooleanField(default=False)

    ### MONGOENGINE META ###

    meta = {
        'indexes': [
            'discogs_id',
            'name',
            '$name',
            ],
        }

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        from discograph.bootstrap import Bootstrap
        cls.drop_collection()
        labels_xml_path = Bootstrap.labels_xml_path
        with gzip.GzipFile(labels_xml_path, 'r') as file_pointer:
            labels_iterator = Bootstrap.iterparse(file_pointer, 'label')
            labels_iterator = Bootstrap.clean_elements(labels_iterator)
            for label_element in labels_iterator:
                label_document = cls.from_element(label_element)
                print(u'LABEL {}: {}'.format(
                    label_document.discogs_id,
                    label_document.name,
                    ))

    def extract_relations(self):
        from discograph import models
        relations = []
        if not self.sublabels:
            return relations
        for sublabel in self.sublabels:
            relation = models.LabelLabelRelation(
                label=sublabel,
                parent_label=self,
                )
            relations.append(relation)
        return relations

    @classmethod
    def from_name(cls, name):
        index = [('name', 1)]
        query_set = cls.objects(name=name).hint(index).only('has_been_scraped')
        count = query_set.count()
        if count:
            assert count == 1
            return query_set[0]
        document = cls(name=name)
        document.save()
        return document

    @classmethod
    def from_element(cls, element):
        name = element.find('name').text
        label_document = cls.from_name(name=name)
        if label_document.has_been_scraped:
            return label_document
        discogs_id = int(element.find('id').text)
        sublabels = element.find('sublabels')
        if sublabels is not None and len(sublabels):
            sublabels = [_.text for _ in sublabels if _.text]
            if sublabels:
                sublabels = [cls.from_name(_) for _ in sublabels]
        else:
            sublabels = []
        parent_label = element.find('parentLabel')
        if parent_label is not None:
            parent_label = parent_label.text
            if parent_label:
                parent_label = cls.from_name(parent_label)
        label_document.discogs_id = discogs_id
        label_document.sublabels = sublabels
        label_document.parent_label = parent_label
        label_document.has_been_scraped = True
        label_document.save()
        return label_document