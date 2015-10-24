# -*- encoding: utf-8 -*-
import collections
import re
import six
from discograph.library.CreditRole import CreditRole
from discograph.library.TrellisNode2 import TrellisNode2
from discograph.library.postgres.PostgresEntity import PostgresEntity


class RelationGrapher2(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_break_on_next_loop',
        '_center_entity',
        '_degree',
        '_entity_keys_to_visit',
        '_link_ratio',
        '_links',
        '_max_nodes',
        '_nodes',
        '_relational_roles',
        '_structural_roles',
        )

    word_pattern = re.compile('\s+')

    ### INITIALIZER ###

    def __init__(
        self,
        center_entity,
        degree=3,
        link_ratio=None,
        max_nodes=None,
        roles=None,
        ):
        assert isinstance(center_entity, PostgresEntity)
        self._center_entity = center_entity
        degree = int(degree)
        assert 0 < degree
        self._degree = degree
        if max_nodes is not None:
            max_nodes = int(max_nodes)
            assert 0 < max_nodes
        else:
            max_nodes = 100
        self._max_nodes = max_nodes
        if link_ratio is not None:
            link_ratio = int(link_ratio)
            assert 0 < link_ratio
        else:
            link_ratio = 3
        self._link_ratio = link_ratio
        roles = roles or None
        if roles:
            if isinstance(roles, six.string_types):
                roles = (roles,)
            elif not isinstance(roles, collections.Iterable):
                roles = (roles,)
            roles = tuple(roles)
            assert all(_ in CreditRole.all_credit_roles for _ in roles)
            structural_roles, relational_roles = [], []
            for role in roles:
                if role in ('Alias', 'Sublabel Of', 'Member Of'):
                    structural_roles.append(role)
                else:
                    relational_roles.append(role)
        self._structural_roles = tuple(structural_roles)
        self._relational_roles = tuple(relational_roles)
        self._nodes = {}
        self._links = {}
        self._break_on_next_loop = False
        self._entity_keys_to_visit = set()

    ### SPECIAL METHODS ###

    def __call__(self):
        self.entity_keys_to_visit.add(self.center_entity.entity_key)
        for distance in range(self.degree + 1):
            entities = PostgresEntity.search_multi(self.entity_keys_to_visit)
            self.entity_keys_to_visit.clear()
            # make a trellis node for each
            # sort by relation counts
            # search from smallest to largest
            # skip large ones, but set their "missing" value
            pass

    ### PUBLIC METHODS ###

    ### PUBLIC PROPERTIES ###

    @property
    def all_roles(self):
        return self.structural_roles + self.relational_roles

    @property
    def break_on_next_loop(self):
        return self._break_on_next_loop

    @break_on_next_loop.setter
    def break_on_next_loop(self, expr):
        self._break_on_next_loop = bool(expr)

    @property
    def center_entity(self):
        return self._center_entity

    @property
    def degree(self):
        return self._degree

    @property
    def entity_keys_to_visit(self):
        return self._entity_keys_to_visit

    @property
    def link_ratio(self):
        return self._link_ratio

    @property
    def links(self):
        return self._links

    @property
    def max_links(self):
        return self._max_nodes * self._link_ratio

    @property
    def max_nodes(self):
        return self._max_nodes

    @property
    def nodes(self):
        return self._nodes

    @property
    def relational_roles(self):
        return self._relational_roles

    @property
    def structural_roles(self):
        return self._structural_roles