# -*- encoding: utf-8 -*-


class TrellisNode(object):

    __slots__ = (
        '_children',
        '_node',
        '_pages',
        '_parents',
        '_parentage',
        '_siblings',
        '_subgraph_size',
        )

    def __init__(self, node):
        self._node = node
        self._parents = set()
        self._siblings = set()
        self._children = set()
        self._subgraph_size = -1
        self._pages = set()
        self._parentage = None

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        return self.entity_key == expr.entity_key

    def __hash__(self):
        return hash((type(self), self.entity_key))

    ### PUBLIC METHODS ###

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
    def distance(self):
        return self._node['distance']

    @property
    def entity_key(self):
        return self._node['key']

    @property
    def children(self):
        return self._children

    @property
    def node(self):
        return self._node

    @property
    def parents(self):
        return self._parents

    @property
    def siblings(self):
        return self._siblings

    @property
    def subgraph_size(self):
        return self._subgraph_size

    @subgraph_size.setter
    def subgraph_size(self, expr):
        self._subgraph_size = int(expr)