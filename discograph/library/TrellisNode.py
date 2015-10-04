# -*- encoding: utf-8 -*-


class TrellisNode(object):

    __slots__ = (
        '_node',
        '_parents',
        '_siblings',
        '_children',
        )

    def __init__(self, node):
        self._node = node
        self._parents = set()
        self._siblings = set()
        self._children = set()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        return self.entity_key == expr.entity_key

    def __hash__(self):
        return hash((type(self), self.entity_key))

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