About Disco/graph
=================

- Interactive sociogram graphing
- Single-page application, using asynchronous calls to a JSON API
- Uses the Discogs XML dump, heavily transformed
- Very mildly popular on Twitter, mostly in Europe

The Stack
---------

The front-end:

- [D3](https://d3js.org): handles svg, animation, force layout
- [Machina-JS](http://machina-js.org/): a finite state machine
- [JQuery](https://jquery.com)
- [Twitter Typeahead](https://github.com/twitter/typeahead.js/)
- [Bootstrap](http://getbootstrap.com/)
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

- *entities* 
- *relations*
