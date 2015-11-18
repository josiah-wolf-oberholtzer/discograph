About Disco/graph
=================

- Interactive sociogram graphing
- Single-page application, using asynchronous calls to a JSON API
- Uses the Discogs XML dump, heavily transformed
- Very mildly popular on Twitter, mostly in Europe

The Stack
---------

The front-end:

- [D3](https://d3js.org): handles svg, animation, and force layout of nodes in the graph
- [Machina-JS](http://machina-js.org/): a finite state machine for simplifying single-page state
- [JQuery](https://jquery.com): mostly just for event binding
- [Twitter Typeahead](https://github.com/twitter/typeahead.js/): for looking up entities
- [Bootstrap](http://getbootstrap.com/): for CSS
- and Grunt, etc.

The back-end:

- Python 3
- [Flask](http://flask.pocoo.org/): a light-weight Werkzeug-based web framework
- [Peewee](http://docs.peewee-orm.com/en/latest/): a light-weight ORM
- PostgreSQL: the primary datastore
- Redis: for caching and rate limiting

The DB Structure
----------------

A classic graph-search problem, with two primary tables: 

- *Entities*: all artists and labels
- *Relations*: any connection drawn between two entities (including the same one)

Relations are extracted from artists, labels and releases:

- aliases
- band membership
- sublabel / parent label

Relation-extraction on releases is a little complicated.

The `entities` table looks like this:

- `entity_type` (1 == Artist, 2 == Label)
- `entity_id` (the Discogs database id)
- `name`
- `random` (random float for easily looking up random entities)
- `metadata` (ANV, profile, etc.)
- `entities` (JSON store of entity IDS for aliases, parent/sublabels, members/groups) (this simplifies many queries)
- `relation_counts` (precomputed counts of # of relations of each time involving this entity, for optimizing graph search)
- `search_content` (full-text-search data)

For example:

```
>>> PostgresEntity.get(entity_type=1, entity_id=1)
PostgresEntity(
    entities={
        'aliases': {
            'Dick Track': 19541,
            'Faxid': 278760,
            'Groove Machine': 16055,
            "Janne Me' Amazonen": 196957,
            'Jesper Dahlbäck': 239,
            'Lenk': 25227,
            'The Pinguin Man': 439150,
            },
        },
    entity_id=1,
    entity_type=1,
    metadata={
        'name_variations': ['Persuader', 'The Presuader'],
        'profile': None,
        'real_name': 'Jesper Dahlbäck',
        },
    name='The Persuader',
    random=0.827062,
    relation_counts={
        'Artwork': 1,
        'Compiled By': 23,
        'Compiled On': 13,
        'Composed By': 2,
        'Copyright (c)': 3,
        'DJ Mix': 30,
        'Design': 1,
        'Distributed By': 2,
        'Drums': 1,
        'Guitar': 2,
        'Lacquer Cut At': 2,
        'Lacquer Cut By': 3,
        'Manufactured By': 1,
        'Mastered At': 4,
        'Mastered By': 4,
        'Music By': 1,
        'Percussion': 1,
        'Phonographic Copyright (p)': 2,
        'Photography By': 2,
        'Pressed By': 1,
        'Produced At': 1,
        'Producer': 3,
        'Published By': 1,
        'Recorded At': 1,
        'Released On': 5,
        'Remix': 13,
        'Written-By': 7,
        },
    search_content="'persuad':2"
    )
```

The `relations` table looks like this:

- `entity_one_type`
- `entity_one_id`
- `entity_two_type` 
- `entity_two_id`
- `release_id`
- `role`
- `year`
- `random`

For example:

```
>>> PostgresRelation.get()
PostgresRelation(
    entity_one_id=370955,
    entity_one_type=1,
    entity_two_id=444541,
    entity_two_type=1,
    random=0.861758,
    release_id=3426859,
    role='Producer',
    year=2004
    )
```
