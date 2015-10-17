# -*- encoding: utf-8 -*-
import random
import re
from abjad.tools import systemtools


urlify_pattern = re.compile(r"\s+", re.MULTILINE)


entity_type_names = {
    1: 'artist',
    2: 'label',
    }


entity_name_types = {
    'artist': 1,
    'label': 2,
    }


def get_entity(entity_type, entity_id):
    import discograph
    where_clause = discograph.SqliteEntity.entity_id == entity_id
    where_clause &= discograph.SqliteEntity.entity_type == entity_type
    query = discograph.SqliteEntity.select().where(where_clause)
    found = list(query)
    if not found:
        return None
    return found[0]


def get_network(entity_id, entity_type, on_mobile=False, cache=True):
    import discograph
    #cache = False
    assert entity_type in ('artist', 'label')
    if cache:
        cache_key = 'discograph:/api/{}/network/{}'
        cache_key = cache_key.format(entity_type, entity_id)
        if on_mobile:
            cache_key = '{}/mobile'.format(cache_key)
        data = discograph.RelationGrapher.cache_get(cache_key)
        if data is not None:
            return data
    entity_type = entity_name_types[entity_type]
    entity = get_entity(entity_type, entity_id)
    if entity is None:
        return None
    roles = [
        'Alias',
        'Member Of',
        'Released On',
        'Sublabel Of',
        ]
    if not on_mobile:
        max_nodes = 75
        degree = 12
    else:
        max_nodes = 25
        degree = 6
    relation_grapher = discograph.RelationGrapher(
        center_entity=entity,
        degree=degree,
        max_nodes=max_nodes,
        roles=roles,
        )
    with systemtools.Timer(exit_message='Network query time:'):
        data = relation_grapher.get_network()
    if cache:
        discograph.RelationGrapher.cache_set(cache_key, data)
    return data


def get_random_entity(roles=None):
    import discograph
    relation = discograph.SqliteRelation.get_random(roles=roles)
    entity_choice = random.randint(1, 2)
    if entity_choice == 1:
        entity_type = relation.entity_one_type
        entity_id = relation.entity_one_id
    else:
        entity_type = relation.entity_two_type
        entity_id = relation.entity_two_id
    return entity_type, entity_id


def parse_request_args(args):
    from discograph.library import CreditRole
    year = None
    roles = set()
    for key in args:
        if key == 'year':
            value = args[key]
            try:
                if '-' in year:
                    start, _, stop = year.partition('-')
                    year = tuple(sorted((int(start), int(stop))))
                else:
                    year = int(year)
            except:
                pass
        elif key == 'roles[]':
            value = args.getlist(key)
            for role in value:
                if role in CreditRole.all_credit_roles:
                    roles.add(role)
    roles = list(sorted(roles))
    return roles, year


def search_entities(search_string, cache=True):
    import discograph
    if cache:
        cache_key = 'discograph:/api/search/{}'.format(
            urlify_pattern.sub('+', search_string))
        data = discograph.RelationGrapher.cache_get(cache_key)
        if data is not None:
            return data
    query = discograph.SqliteFTSEntity.search_bm25(search_string).limit(10)
    data = []
    for entity in query:
        datum = dict(
            key='{}-{}'.format(
                entity_type_names[entity.entity_type],
                entity.entity_id,
                ),
            name=entity.name,
            )
        data.append(datum)
        print('    {}'.format(datum))
    data = {'results': tuple(data)}
    if cache:
        discograph.RelationGrapher.cache_set(cache_key, data)
    return data