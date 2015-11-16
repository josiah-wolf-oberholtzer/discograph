# -*- encoding: utf-8 -*-
import multiprocessing
import peewee
import time
from abjad.tools import stringtools
from abjad.tools import systemtools
from playhouse import postgres_ext
from discograph.library.Bootstrapper import Bootstrapper
from discograph.library.PostgresModel import PostgresModel


class PostgresEntity(PostgresModel):

    ### CLASS VARIABLES ###

    class BootstrapWorker(multiprocessing.Process):

        corpus = {}

        def __init__(self, queue):
            multiprocessing.Process.__init__(self)
            self.queue = queue

        def run(self):
            proc_name = self.name
            while True:
                task = self.queue.get()
                if task is None:
                    self.queue.task_done()
                    break
                entity_type, entity_id = task
                PostgresEntity.bootstrap_pass_three_single(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    )
                self.queue.task_done()

    ### PEEWEE FIELDS ###

    entity_id = peewee.IntegerField()
    entity_type = peewee.IntegerField()
    name = peewee.TextField(index=True)
    relation_counts = postgres_ext.BinaryJSONField(null=True)
    metadata = postgres_ext.BinaryJSONField(null=True)
    entities = postgres_ext.BinaryJSONField(null=True)
    search_content = postgres_ext.TSVectorField()

    ### PEEWEE META ###

    class Meta:
        db_table = 'entities'
        primary_key = peewee.CompositeKey('entity_type', 'entity_id')

    ### PUBLIC METHODS ###

    @classmethod
    def bootstrap(cls):
        cls.drop_table(True)
        cls.create_table()
        cls.bootstrap_pass_one()
        cls.bootstrap_pass_two()

    @classmethod
    def bootstrap_pass_one(cls):
        PostgresModel.bootstrap_pass_one(
            cls,
            'artist',
            name_attr='name',
            skip_without=['name'],
            )
        PostgresModel.bootstrap_pass_one(
            cls,
            'label',
            name_attr='name',
            skip_without=['name'],
            )

    @classmethod
    def get_entity_iterator(cls, entity_type):
        id_query = cls.select(peewee.fn.Max(cls.entity_id))
        id_query = id_query.where(cls.entity_type == entity_type)
        max_id = id_query.scalar()
        for i in range(1, max_id + 1):
            query = cls.select().where(cls.entity_id == i, cls.entity_type == entity_type)
            if not query.count():
                continue
            document = query.get()
            yield document

    @classmethod
    def bootstrap_pass_two(cls):
        skipped_template = u'{} [SKIPPED] (Pass 2) (id:{}) [{:.8f}]: {}'
        changed_template = u'{}           (Pass 2) (id:{}) [{:.8f}]: {}'
        corpus = {}
        for document in cls.get_entity_iterator(entity_type=1):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references(corpus)
            if not changed:
                message = skipped_template.format(
                    cls.__name__.upper(),
                    (document.entity_type, document.entity_id),
                    timer.elapsed_time,
                    document.name,
                    )
                print(message)
                continue
            document.save()
            message = changed_template.format(
                cls.__name__.upper(),
                (document.entity_type, document.entity_id),
                timer.elapsed_time,
                document.name,
                )
            print(message)
        corpus = {}
        for document in cls.get_entity_iterator(entity_type=2):
            with systemtools.Timer(verbose=False) as timer:
                changed = document.resolve_references(corpus)
            if not changed:
                message = skipped_template.format(
                    cls.__name__.upper(),
                    (document.entity_type, document.entity_id),
                    timer.elapsed_time,
                    document.name,
                    )
                print(message)
                continue
            document.save()
            message = changed_template.format(
                cls.__name__.upper(),
                (document.entity_type, document.entity_id),
                timer.elapsed_time,
                document.name,
                )
            print(message)

    @classmethod
    def bootstrap_pass_three(cls):
        queue = multiprocessing.JoinableQueue()
        workers = [cls.BootstrapWorker(queue) for _ in range(4)]
        for worker in workers:
            worker.start()
        entity_type = 1
        artist_id_query = cls.select(peewee.fn.Max(cls.entity_id))
        artist_id_query = artist_id_query.where(cls.entity_type == entity_type)
        max_artist_id = artist_id_query.scalar()
        for entity_id in range(1, max_artist_id + 1):
            while not queue.empty():
                time.sleep(0.0001)
            queue.put((entity_type, entity_id))
        entity_type = 2
        label_id_query = cls.select(peewee.fn.Max(cls.entity_id))
        label_id_query = label_id_query.where(cls.entity_type == entity_type)
        max_label_id = label_id_query.scalar()
        for entity_id in range(1, max_label_id + 1):
            while not queue.empty():
                time.sleep(0.0001)
            queue.put((entity_type, entity_id))
        for worker in workers:
            queue.put(None)
        queue.join()
        queue.close()
        for worker in workers:
            worker.join()
        for worker in workers:
            worker.terminate()

    @classmethod
    def bootstrap_pass_three_single(cls, entity_type, entity_id):
        import discograph
        template = u'{} (Pass 3) (id:{}) {}: {}'
        query = cls.select().where(
            cls.entity_id == entity_id, 
            cls.entity_type == entity_type,
            )
        if not query.count():
            return
        document = query.get()
        entity_id = document.entity_id
        where_clause = (
            (discograph.PostgresRelation.entity_one_id == entity_id) &
            (discograph.PostgresRelation.entity_one_type == entity_type)
            )
        where_clause |= (
            (discograph.PostgresRelation.entity_two_id == entity_id) &
            (discograph.PostgresRelation.entity_two_type == entity_type)
            )
        query = discograph.PostgresRelation.select().where(where_clause)
        relation_counts = {}
        for relation in query:
            if relation.role not in relation_counts:
                relation_counts[relation.role] = set()
            key = (
                relation.entity_one_type,
                relation.entity_one_id,
                relation.entity_two_type,
                relation.entity_two_id,
                )
            relation_counts[relation.role].add(key)
        for role, keys in relation_counts.items():
            relation_counts[role] = len(keys)
        if not relation_counts:
            return
        document.relation_counts = relation_counts
        document.save()
        message = template.format(
            cls.__name__.upper(),
            (document.entity_type, document.entity_id),
            document.name,
            len(relation_counts),
            )
        print(message)

    @classmethod
    def element_to_names(cls, names):
        result = {}
        if names is None or not len(names):
            return result
        for name in names:
            name = name.text
            if not name:
                continue
            result[name] = None
        return result

    @classmethod
    def element_to_names_and_ids(cls, names_and_ids):
        result = {}
        if names_and_ids is None or not len(names_and_ids):
            return result
        for i in range(0, len(names_and_ids), 2):
            discogs_id = int(names_and_ids[i].text)
            name = names_and_ids[i + 1].text
            result[name] = discogs_id
        return result

    @classmethod
    def element_to_parent_label(cls, parent_label):
        result = {}
        if parent_label is None or parent_label.text is None:
            return result
        name = parent_label.text.strip()
        if not name:
            return result
        result[name] = None
        return result

    @classmethod
    def element_to_sublabels(cls, sublabels):
        result = {}
        if sublabels is None or not len(sublabels):
            return result
        for sublabel in sublabels:
            name = sublabel.text
            if name is None:
                continue
            name = name.strip()
            if not name:
                continue
            result[name] = None
        return result

    @classmethod
    def fixup_search_content(cls):
        template = 'FIXUP ({}:{}): {}'
        for document in cls.get_entity_iterator(entity_type=1):
            search_content = document.name
            search_content = search_content.lower()
            search_content = stringtools.strip_diacritics(search_content)
            document.search_content = peewee.fn.to_tsvector(search_content)
            document.save()
            message = template.format(
                document.entity_type,
                document.entity_id,
                document.name,
                )
            print(message)
        for document in cls.get_entity_iterator(entity_type=2):
            search_content = document.name
            search_content = search_content.lower()
            search_content = stringtools.strip_diacritics(search_content)
            document.search_content = search_content
            document.save()
            message = template.format(
                document.entity_type,
                document.entity_id,
                document.name,
                )
            print(message)

    @classmethod
    def from_element(cls, element):
        data = cls.tags_to_fields(element)
        return cls(**data)

    @classmethod
    def preprocess_data(cls, data, element):
        data['metadata'] = {}
        data['entities'] = {}
        for key in (
            'aliases',
            'groups',
            'members',
            'parent_label',
            'sublabels',
            ):
            if key in data:
                data['entities'][key] = data.pop(key)
        for key in (
            'contact_info',
            'name_variations',
            'profile',
            'real_name',
            'urls',
            ):
            if key in data:
                data['metadata'][key] = data.pop(key)
        if 'name' in data and data.get('name'):
            search_content = data.get('name')
            search_content = search_content.lower()
            search_content = stringtools.strip_diacritics(search_content)
            data['search_content'] = peewee.fn.to_tsvector(search_content)
        if element.tag == 'artist':
            data['entity_type'] = 1
        elif element.tag == 'label':
            data['entity_type'] = 2
        return data

    def resolve_references(self, corpus):
        changed = False
        if self.entity_type == 1:
            entity_type = 1
            for section in ('aliases', 'groups', 'members'):
                if section not in self.entities:
                    continue
                for entity_name in self.entities[section].keys():
                    key = (entity_type, entity_name)
                    self.update_corpus(corpus, key)
                    if key in corpus:
                        self.entities[section][entity_name] = corpus[key]
                        changed = True
        elif self.entity_type == 2:
            entity_type = 2
            for section in ('parent_label', 'sublabels'):
                if section not in self.entities:
                    continue
                for entity_name in self.entities[section].keys():
                    key = (entity_type, entity_name)
                    self.update_corpus(corpus, key)
                    if key in corpus:
                        self.entities[section][entity_name] = corpus[key]
                        changed = True
        return changed

    def roles_to_relation_count(self, roles):
        count = 0
        relation_counts = self.relation_counts or {}
        for role in roles:
            if role == 'Alias':
                count += len(self.entities.get('aliases', ()))
            elif role == 'Member Of':
                count += len(self.entities.get('groups', ()))
                count += len(self.entities.get('members', ()))
            elif role == 'Sublabel Of':
                count += len(self.entities.get('parent_label', ()))
                count += len(self.entities.get('sublabels', ()))
            else:
                count += relation_counts.get(role, 0)
        return count

    @classmethod
    def search_multi(cls, entity_keys):
        artist_ids, label_ids = [], []
        for entity_type, entity_id in entity_keys:
            if entity_type == 1:
                artist_ids.append(entity_id)
            elif entity_type == 2:
                label_ids.append(entity_id)
        if artist_ids and label_ids:
            where_clause = (
                (
                    (cls.entity_type == 1) &
                    (cls.entity_id.in_(artist_ids))
                    ) | (
                    (cls.entity_type == 2) &
                    (cls.entity_id.in_(label_ids))
                    )
                )
        elif artist_ids:
            where_clause = (
                (cls.entity_type == 1) &
                (cls.entity_id.in_(artist_ids))
                )
        else:
            where_clause = (
                (cls.entity_type == 2) &
                (cls.entity_id.in_(label_ids))
                )
        return cls.select().where(where_clause)

    @classmethod
    def search_text(cls, search_string):
        search_string = search_string.lower()
        search_string = stringtools.strip_diacritics(search_string)
        search_string = ','.join(search_string.split())
        query = PostgresEntity.select()
        query = query.where(PostgresEntity.search_content.match(search_string))
        return query 

    def structural_roles_to_entity_keys(self, roles):
        entity_keys = set()
        if self.entity_type == 1:
            entity_type = 1
            if 'Alias' in roles:
                for section in ('aliases',):
                    if section not in self.entities:
                        continue
                    for entity_id in self.entities[section].values():
                        if not entity_id:
                            continue
                        entity_keys.add((entity_type, entity_id))
            if 'Member Of' in roles:
                for section in ('groups', 'members'):
                    if section not in self.entities:
                        continue
                    for entity_id in self.entities[section].values():
                        if not entity_id:
                            continue
                        entity_keys.add((entity_type, entity_id))
        elif self.entity_type == 2:
            entity_type = 2
            if 'Sublabel Of' in roles:
                for section in ('parent_label', 'sublabels'):
                    if section not in self.entities:
                        continue
                    for entity_id in self.entities[section].values():
                        if not entity_id:
                            continue
                        entity_keys.add((entity_type, entity_id))
        return entity_keys

    def structural_roles_to_relations(self, roles):
        from discograph import PostgresRelation
        relations = {}
        if self.entity_type == 1:
            entity_type = 1
            role = 'Alias'
            if role in roles and 'aliases' in self.entities:
                for entity_id in self.entities['aliases'].values():
                    if not entity_id:
                        continue
                    ids = sorted((entity_id, self.entity_id))
                    relation = PostgresRelation(
                        entity_one_type=entity_type,
                        entity_one_id=ids[0],
                        entity_two_type=entity_type,
                        entity_two_id=ids[1],
                        role=role,
                        )
                    relations[relation.link_key] = relation
            role = 'Member Of'
            if role in roles:
                if 'groups' in self.entities:
                    for entity_id in self.entities['groups'].values():
                        if not entity_id:
                            continue
                        relation = PostgresRelation(
                            entity_one_type=entity_type,
                            entity_one_id=self.entity_id,
                            entity_two_type=entity_type,
                            entity_two_id=entity_id,
                            role=role,
                            )
                        relations[relation.link_key] = relation
                if 'members' in self.entities:
                    for entity_id in self.entities['members'].values():
                        if not entity_id:
                            continue
                        relation = PostgresRelation(
                            entity_one_type=entity_type,
                            entity_one_id=entity_id,
                            entity_two_type=entity_type,
                            entity_two_id=self.entity_id,
                            role=role,
                            )
                        relations[relation.link_key] = relation
        elif self.entity_type == 2 and 'Sublabel Of' in roles:
            entity_type = 2
            role = 'Sublabel Of'
            if 'parent_label' in self.entities:
                for entity_id in self.entities['parent_label'].values():
                    if not entity_id:
                        continue
                    relation = PostgresRelation(
                        entity_one_type=entity_type,
                        entity_one_id=self.entity_id,
                        entity_two_type=entity_type,
                        entity_two_id=entity_id,
                        role=role,
                        )
                    relations[relation.link_key] = relation
            if 'sublabels' in self.entities:
                for entity_id in self.entities['sublabels'].values():
                    if not entity_id:
                        continue
                    relation = PostgresRelation(
                        entity_one_type=entity_type,
                        entity_one_id=entity_id,
                        entity_two_type=entity_type,
                        entity_two_id=self.entity_id,
                        role=role,
                        )
                    relations[relation.link_key] = relation
        return relations

    @classmethod
    def update_corpus(cls, corpus, key):
        if key in corpus:
            return
        entity_type, entity_name = key
        query = cls.select().where(
            cls.entity_type == entity_type,
            cls.name == entity_name,
            )
        if query.count():
            corpus[key] = query.get().entity_id

    ### PUBLIC PROPERTIES ###

    @property
    def entity_key(self):
        return (self.entity_type, self.entity_id)

    @property
    def json_entity_key(self):
        entity_type, entity_id = self.entity_key
        if entity_type == 1:
            return 'artist-{}'.format(self.entity_id)
        elif entity_type == 2:
            return 'label-{}'.format(self.entity_id)
        raise ValueError(self.entity_key)

    @property
    def size(self):
        if self.entity_type == 1:
            members = self.entities.get('members', ())
        elif self.entity_type == 2:
            members = self.entities.get('sublabels', ())
        return len(members)

PostgresEntity._tags_to_fields_mapping = {
    'aliases': ('aliases', PostgresEntity.element_to_names),
    'contact_info': ('contact_info', Bootstrapper.element_to_string),
    'groups': ('groups', PostgresEntity.element_to_names),
    'id': ('entity_id', Bootstrapper.element_to_integer),
    'members': ('members', PostgresEntity.element_to_names_and_ids),
    'name': ('name', Bootstrapper.element_to_string),
    'namevariations': ('name_variations', Bootstrapper.element_to_strings),
    'parentLabel': ('parent_label', PostgresEntity.element_to_parent_label),
    'profile': ('profile', Bootstrapper.element_to_string),
    'realname': ('real_name', Bootstrapper.element_to_string),
    'sublabels': ('sublabels', PostgresEntity.element_to_sublabels),
    'urls': ('urls', Bootstrapper.element_to_strings),
    }