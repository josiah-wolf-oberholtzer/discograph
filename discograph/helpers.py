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


args_roles_pattern = re.compile(r'^roles(\[\d*\])?$')


def get_entity(entity_type, entity_id):
    import discograph
    where_clause = discograph.PostgresEntity.entity_id == entity_id
    where_clause &= discograph.PostgresEntity.entity_type == entity_type
    with discograph.PostgresModel._meta.database.execution_context():
        query = discograph.PostgresEntity.select().where(where_clause)
        if not query.count():
            return None
        return query.get()


def get_network(entity_id, entity_type, on_mobile=False, cache=True, roles=None):
    import discograph
    assert entity_type in ('artist', 'label')
    template = 'discograph:/api/{entity_type}/network/{entity_id}'
    cache_key = discograph.RelationGrapher.make_cache_key(
        template,
        entity_type,
        entity_id,
        roles=roles,
        )
    if on_mobile:
        template = '{}/mobile'.format(template)
    cache_key = cache_key.format(entity_type, entity_id)
    cache = False
    if cache:
        data = discograph.RelationGrapher.cache_get(cache_key)
        if data is not None:
            return data
    entity_type = entity_name_types[entity_type]
    entity = get_entity(entity_type, entity_id)
    if entity is None:
        return None
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
        with discograph.PostgresModel._meta.database.execution_context():
            data = relation_grapher()
    if cache:
        discograph.RelationGrapher.cache_set(cache_key, data)
    return data


def get_random_entity(roles=None):
    import discograph
    structural_roles = [
        'Alias',
        'Member Of',
        'Sublabel Of',
        ]
    if roles and any(_ not in structural_roles for _ in roles):
        with discograph.PostgresModel._meta.database.execution_context():
            relation = discograph.PostgresRelation.get_random(roles=roles)
        entity_choice = random.randint(1, 2)
        if entity_choice == 1:
            entity_type = relation.entity_one_type
            entity_id = relation.entity_one_id
        else:
            entity_type = relation.entity_two_type
            entity_id = relation.entity_two_id
    else:
        with discograph.PostgresModel._meta.database.execution_context():
            entity = discograph.PostgresEntity.get_random()
        entity_type, entity_id = entity.entity_type, entity.entity_id
    return entity_type, entity_id


def get_relations(entity_id, entity_type):
    import discograph
    if isinstance(entity_type, str):
        entity_type = entity_name_types[entity_type]
    entity = get_entity(entity_type, entity_id)
    if entity is None:
        return None
    with discograph.PostgresModel._meta.database.execution_context():
        query = discograph.PostgresRelation.search(
            entity_id=entity.entity_id,
            entity_type=entity.entity_type,
            query_only=True
            )
    query = query.order_by(
        discograph.PostgresRelation.role,
        discograph.PostgresRelation.entity_one_id,
        discograph.PostgresRelation.entity_one_type,
        discograph.PostgresRelation.entity_two_id,
        discograph.PostgresRelation.entity_two_type,
        )
    data = []
    for relation in query:
        category = discograph.CreditRole.all_credit_roles[relation.role]
        if category is None:
            continue
        category = category[0]
        datum = {
            'role': relation.role,
            }
        data.append(datum)
    data = {'results': tuple(data)}
    return data


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
        elif args_roles_pattern.match(key):
            value = args.getlist(key)
            for role in value:
                if role in CreditRole.all_credit_roles:
                    roles.add(role)
    roles = list(sorted(roles))
    return roles, year


def search_entities(search_string, cache=True):
    import discograph
    cache_key = 'discograph:/api/search/{}'.format(
        urlify_pattern.sub('+', search_string))
    cache = False
    if cache:
        data = discograph.RelationGrapher.cache_get(cache_key)
        if data is not None:
            print('{}: CACHED'.format(cache_key))
            for datum in data['results']:
                print('    {}'.format(datum))
            return data
    with discograph.PostgresModel._meta.database.execution_context():
        query = discograph.PostgresEntity.search_text(search_string)
        print('{}: NOT CACHED'.format(cache_key))
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