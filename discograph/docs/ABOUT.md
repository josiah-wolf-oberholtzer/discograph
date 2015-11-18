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

Relation-extraction on releases is a little complicated. Relations need to be drawn appropriately between artists, labels, companies, release-global extra-artists, track artists, track extra-artists, etc. Who did what role for whom?

The `entities` table looks like this:

- `entity_type` (1 == Artist, 2 == Label)
- `entity_id` (the Discogs database id)
- `name`
- `random` (random float for efficiently looking up random entities)
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
- `release_id` (will soon be migrated to a JSON store to reduce the number of rows in the relations table, by collapsing relations with identical entities and roles into a single row of multiple releases)
- `role` (the credit role)
- `year` (currently just aspirational)
- `random` (random float for efficiently looking up random relations)

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

The graph-search algorithm
--------------------------

Here's the terminal output for the graph-search, starting with Morris Day, and using the roles "Alias", "Member Of" and "Guitar":

```
Searching around Morris Day...
    Max nodes: 75
    Max links: 225
    Roles: ('Alias', 'Member Of', 'Guitar')
    At distance 0:
        0 old nodes
        0 old links
        1 new nodes
        Retrieving entities
            1-1 of 1
        Retrieving structural relations
        Retrieving relational relations
            1-1 of 1
    At distance 1:
        1 old nodes
        8 old links
        8 new nodes
        Retrieving entities
            1-8 of 8
        Retrieving structural relations
        Retrieving relational relations
            1-8 of 8
    At distance 2:
        9 old nodes
        188 old links
        161 new nodes
        Retrieving entities
            1-161 of 161
        Max nodes: exiting next search loop.
        Retrieving structural relations
        Max links: exiting next search loop.
    At distance 3:
        170 old nodes
        833 old links
        584 new nodes
        Retrieving entities
            1-584 of 584
    Cross-referencing...
        753 & 753
        Cross-referenced: 754 nodes / 1060 links
    Built trellis: 754 nodes / 1060 links
    Partitioning trellis into 11 pages...
        Maximum: 75 nodes / 225 links
        Maximum depth: 3
        Subgraph threshold: 17.136363636363637
            At distance 0: 754.0 geometric mean
            At distance 1: 2.306143078159937 geometric mean
            At distance 2: 1.0427629961486573 geometric mean
            At distance 3: 1.0109670668659374 geometric mean
                Testing 754.0 @ distance 0
                Testing 2.306143078159937 @ distance 1
            Winning distance: 1
        Paging by local neighborhood: 9
        Paging at winning distance...
        Paging by distance...
        Page 0: 104
        Page 1: 103
        Page 2: 103
        Page 3: 103
        Page 4: 103
        Page 5: 103
        Page 6: 103
        Page 7: 103
        Page 8: 103
        Page 9: 104
        Page 10: 104
Network query time: 0.6372168064117432
```
