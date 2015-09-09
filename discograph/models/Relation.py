import collections
import itertools
import mongoengine
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from discograph.models.Model import Model
from discograph.models.Artist import Artist
from discograph.models.Label import Label


class Relation(Model, mongoengine.Document):

    ### CLASS VARIABLES ###

    Reference = collections.namedtuple(
        'Reference',
        ['class_', 'discogs_id', 'name'],
        )

    class EntityType(datastructuretools.Enumeration):
        ARTIST = 1
        LABEL = 2

    _model_to_entity_type = {
        Artist: EntityType.ARTIST,
        Label: EntityType.LABEL,
        }

    ### MONGOENGINE FIELDS ###

    entity_one_id = mongoengine.IntField()
    entity_one_name = mongoengine.StringField()
    entity_one_type = mongoengine.IntField()
    entity_two_id = mongoengine.IntField()
    entity_two_name = mongoengine.StringField()
    entity_two_type = mongoengine.IntField()
    role_name = mongoengine.StringField()
    category = mongoengine.IntField()
    subcategory = mongoengine.IntField(null=True)
    is_trivial = mongoengine.BooleanField()
    release_id = mongoengine.IntField(null=True)
    year = mongoengine.IntField(null=True)

    ### MONOGENGINE META ###

    meta = {
        'indexes': [
            '#entity_one_name',
            '#entity_two_name',
            '#role_name',
            'role_name',
            'category',
            'entity_one_id',
            'entity_one_type',
            'entity_two_id',
            'entity_two_type',
            'release_id',
            'subcategory',
            'year',
            ]
        }

    ### PRIVATE METHODS ###

    @classmethod
    def _get_categories(cls, role_name):
        from discograph import models
        categories = models.ArtistRole._available_credit_roles.get(
            role_name, None)
        if not categories:
            return None, None
        if len(categories) == 1:
            return categories[0], None
        return categories

    @classmethod
    def _partition_artists(cls, artists):
        pass

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from discograph import models
        keyword_argument_names = sorted(self._fields)
        if 'id' in keyword_argument_names:
            keyword_argument_names.remove('id')
        keyword_argument_callables = dict(
            category=models.ArtistRole.Category,
            entity_one_type=self.EntityType,
            entity_two_type=self.EntityType,
            subcategory=models.ArtistRole.Subcategory,
            )
        for keyword_argument_name in keyword_argument_names[:]:
            value = getattr(self, keyword_argument_name)
            if isinstance(value, list) and not value:
                keyword_argument_names.remove(keyword_argument_name)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=keyword_argument_names,
            keyword_argument_callables=keyword_argument_callables,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def model_to_tuple(cls, reference):
        from discograph import models
        if isinstance(reference, cls.Reference):
            return reference
        class_ = models.Artist
        prototype = (
            models.Label,
            models.LabelCredit,
            models.LabelReference,
            )
        if isinstance(reference, prototype):
            class_ = models.Label
        result = cls.Reference(
            class_=class_,
            discogs_id=reference.discogs_id,
            name=reference.name,
            )
        #print(reference, result)
        return result

    @classmethod
    def bootstrap(cls):
        #cls.drop_collection()
        #cls.bootstrap_pass_one()
        #cls.bootstrap_pass_two()
        cls.bootstrap_pass_three()

    @classmethod
    def bootstrap_pass_one(cls):
        from discograph import models
        query = models.Artist.objects.no_cache().timeout(False)
        for i, artist in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                artist.discogs_id,
                artist.name,
                ))
            for relation in cls.from_artist(artist):
                relation.save_if_unique()

    @classmethod
    def bootstrap_pass_two(cls):
        from discograph import models
        query = models.Label.objects.no_cache().timeout(False)
        for i, label in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                label.discogs_id,
                label.name,
                ))
            for relation in cls.from_label(label):
                relation.save_if_unique()

    @classmethod
    def bootstrap_pass_three(cls):
        from discograph import models
        query = models.Release.objects.no_cache().timeout(False)
        for i, release in enumerate(query):
            print('(idx:{}) (id:{}) {}'.format(
                i,
                release.discogs_id,
                release.title,
                ))
            for relation in cls.from_release(release):
                relation.save_if_unique()

    @classmethod
    def from_artist(cls, artist):
        triples = set()
        role = 'Alias'
        for alias in artist.aliases:
            if not alias.discogs_id:
                continue
            artist_one, artist_two = sorted(
                [artist, alias],
                key=lambda x: x.discogs_id,
                )
            entity_one = cls.model_to_tuple(artist_one)
            entity_two = cls.model_to_tuple(artist_two)
            triples.add((entity_one, role, entity_two))
        role = 'Member Of'
        for member in artist.members:
            entity_one = cls.model_to_tuple(member)
            entity_two = cls.model_to_tuple(artist)
            triples.add((entity_one, role, entity_two))
        key_function = lambda x: (x[0].discogs_id, x[1], x[2].discogs_id)
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

    @classmethod
    def from_label(cls, label):
        if not label.discogs_id:
            return []
        triples = set()
        role = 'Sublabel Of'
        for sublabel in label.sublabels:
            if not sublabel.discogs_id:
                continue
            entity_one = cls.model_to_tuple(sublabel)
            entity_two = cls.model_to_tuple(label)
            triples.add((entity_one, role, entity_two))
        key_function = lambda x: (x[0].discogs_id, x[1], x[2].discogs_id)
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples)
        return relations

    @classmethod
    def from_triples(cls, triples, release=None):
        from discograph import models
        #for triple in triples:
        #    print(triple)
        relations = []
        release_id, year = None, None
        if release is not None:
            release_id = release.discogs_id
            if release.release_date is not None:
                year = release.release_date.year
        for entity_one, role_name, entity_two in triples:
            entity_one_type = cls.EntityType.ARTIST
            if issubclass(entity_one.class_, (models.Label, models.LabelReference)):
                entity_one_type = cls.EntityType.LABEL
            entity_two_type = cls.EntityType.ARTIST
            if issubclass(entity_two.class_, (models.Label, models.LabelReference)):
                entity_two_type = cls.EntityType.LABEL
            category, subcategory = cls._get_categories(role_name)
            is_trivial = None
            if (
                entity_one_type == entity_two_type == cls.EntityType.ARTIST and
                role_name not in ('Member Of', 'Alias')
                ):
                pass
                #if entity_one.discogs_id == entity_two.discogs_id:
                #    is_trivial = True
                #if entity_one in entity_two.members:
                #    is_trivial = True
                #if entity_one.name in entity_two.aliases:
                #    is_trivial = True
                #if entity_two.name in entity_one.aliases:
                #    is_trivial = True
            relation = cls(
                category=category,
                entity_one_id=entity_one.discogs_id,
                entity_one_name=entity_one.name,
                entity_one_type=entity_one_type,
                entity_two_id=entity_two.discogs_id,
                entity_two_name=entity_two.name,
                entity_two_type=entity_two_type,
                release_id=release_id,
                role_name=role_name,
                subcategory=subcategory,
                year=year,
                is_trivial=is_trivial,
                )
            relations.append(relation)
        return relations

    @classmethod
    def from_release(cls, release):
        from discograph import models

        triples = set()
        is_compilation = False
        artists = set(cls.model_to_tuple(_) for _ in release.artists)
        labels = set(cls.model_to_tuple(_) for _ in release.labels)
        if len(artists) == 1 and list(artists)[0].name == 'Various':
            is_compilation = True
            artists.clear()
            for track in release.tracklist:
                artists.update(cls.model_to_tuple(_) for _ in track.artists)
        for format_ in release.formats:
            for description in format_.descriptions:
                if description == 'Compilation':
                    is_compilation = True
                    break

        # Handle Artist-Label release relations.
        iterator = itertools.product(artists, labels)
        if is_compilation:
            role = 'Compiled On'
        else:
            role = 'Released On'
        for artist, label in iterator:
            entity_one = cls.model_to_tuple(artist)
            entity_two = cls.model_to_tuple(label)
            triples.add((entity_one, role, entity_two))

        # TODO: Filter out "Hosted By", "Presenter", "DJ Mix", "Compiled By"
        aggregate_roles = {}
        aggregate_role_names = (
            'Compiled By',
            'Curated By',
            'DJ Mix',
            'Hosted By',
            'Presenter',
            )

        # Handle release-global extra artists.
        if is_compilation:
            iterator = itertools.product(labels, release.extra_artists)
        else:
            iterator = itertools.product(artists, release.extra_artists)
        for entity_two, credit in iterator:
            entity_two = cls.model_to_tuple(entity_two)
            for role in credit.roles:
                role_name = role.name
                if role_name not in models.ArtistRole._available_credit_roles:
                    continue
                elif role_name in aggregate_role_names:
                    if role_name not in aggregate_roles:
                        aggregate_roles[role_name] = []
                    aggregate_roles[role_name].append(credit)
                    continue
                entity_one = cls.model_to_tuple(credit)
                triples.add((entity_one, role_name, entity_two))

        # Handle extra artists on individual tracks.
        all_track_artists = set()
        for track in release.tracklist:
            track_artists = set(cls.model_to_tuple(_) for _ in track.artists)
            all_track_artists.update(track_artists)
            track_artists = track_artists or artists or labels
            iterator = itertools.product(track_artists, track.extra_artists)
            for entity_two, credit in iterator:
                entity_two = cls.model_to_tuple(entity_two)
                for role in credit.roles:
                    role_name = role.name
                    if role_name not in models.ArtistRole._available_credit_roles:
                        continue
                    entity_one = cls.model_to_tuple(credit)
                    triples.add((entity_one, role_name, entity_two))

        # Handle aggregate artists (DJ, Compiler, Curator, Presenter, etc.)
        for role_name, aggregate_artists in aggregate_roles.items():
            iterator = itertools.product(all_track_artists, aggregate_artists)
            for track_artist, aggregate_artist in iterator:
                entity_one = cls.model_to_tuple(aggregate_artist)
                entity_two = cls.model_to_tuple(track_artist)
                triples.add((entity_one, role_name, entity_two))

        key_function = lambda x: (
            getattr(x[0], 'discogs_id', 0) or 0,
            getattr(x[2], 'discogs_id', 0) or 0,
            x[1],
            x[0].name,
            x[2].name,
            )
        triples = sorted(triples, key=key_function)
        relations = cls.from_triples(triples, release=release)
        return relations

    def save_if_unique(self):
        query = type(self).objects(
            entity_one_id=self.entity_one_id,
            entity_one_type=self.entity_one_type,
            entity_two_id=self.entity_two_id,
            entity_two_type=self.entity_two_type,
            role_name=self.role_name,
            release_id=self.release_id,
            )
        if query.count():
            print('    SKIPPING {!r} : {} : {!r}'.format(
                self.entity_one_name, self.role_name, self.entity_two_name)
                )
        else:
            print('    {!r} : {} : {!r}'.format(
                self.entity_one_name, self.role_name, self.entity_two_name)
                )
            self.save()