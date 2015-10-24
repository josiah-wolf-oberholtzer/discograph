# -*- encoding: utf-8 -*-


class TrellisNode2(object):

    __slots__ = (
        '_children',
        '_cluster',
        '_links',
        '_missing',
        '_missing_by_page',
        '_entity',
        '_pages',
        '_parents',
        '_parentage',
        '_siblings',
        '_subgraph_size',
        '_distance',
        '_links',
        )

    def __init__(self, entity, distance=0):
        self._children = set()
        self._cluster = 0
        self._distance = distance
        self._links = set()
        self._missing = 0
        self._missing_by_page = {}
        self._entity = entity
        self._pages = set()
        self._parentage = None
        self._parents = set()
        self._siblings = set()
        self._subgraph_size = None

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        return self.entity_key == expr.entity_key

    def __hash__(self):
        return hash((type(self), self.entity_key))

    ### PUBLIC METHODS ###

    def get_neighbors(self):
        neighbors = set()
        neighbors.update(self.parents)
        for sibling in self.siblings:
            if sibling.pages.intersection(self.pages):
                neighbors.add(sibling)
        neighbors.update(self.children)
        return neighbors

    def get_parentage(self):
        if self._parentage is not None:
            return self._parentage
        parentage = set([self])
        parents = self.parents
        while parents:
            parentage.update(parents)
            new_parents = set()
            for parent in parents:
                new_parents.update(parent.parents)
            parents = new_parents
        parentage = frozenset(parentage)
        self._parentage = parentage
        return parentage

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return self._children

    @property
    def cluster(self):
        return self._cluster

    @cluster.setter
    def cluster(self, expr):
        self._cluster = int(expr)

    @property
    def distance(self):
        return self._distance

    @property
    def entity(self):
        return self._entity

    @property
    def entity_key(self):
        return self._entity.entity_key

    @property
    def links(self):
        return self._links

    @property
    def missing(self):
        return self._missing

    @missing.setter
    def missing(self, expr):
        self._missing = int(expr)

    @property
    def missing_by_page(self):
        return self._missing_by_page

    @property
    def pages(self):
        return self._pages

    @property
    def parents(self):
        return self._parents

    @property
    def siblings(self):
        return self._siblings

    @property
    def size(self):
        return self._entity.size

    @property
    def subgraph_size(self):
        return self._subgraph_size

    @subgraph_size.setter
    def subgraph_size(self, expr):
        self._subgraph_size = int(expr)