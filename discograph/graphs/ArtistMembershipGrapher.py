import math
from abjad import documentationtools
from discograph import models


# TODO: add all aliases within same degree (they should have relative degree 0)
# TODO: match discogs id against name and degree (use dict, not set).


class ArtistMembershipGrapher(object):

    ### INITIALIZER ###

    def __init__(self, artists, degree=3, cache=None, max_nodes=None):
        assert len(artists)
        assert all(isinstance(_, models.Artist) for _ in artists)
        assert 0 < int(degree)
        self.artists = tuple(artists)
        self.degree = int(degree)
        self.cache = cache
        self.max_nodes = max_nodes

    ### SPECIAL METHODS ###

    def __graph__(self):
        nodes, edges = self.get_network()
        artist_id_to_node_mapping = {}
        cluster_id_to_cluster_mapping = {}
        graphviz_graph = documentationtools.GraphvizGraph(
            attributes=dict(
                bgcolor='transparent',
                fontname='Arial',
                output_order='edgesfirst',
                overlap='prism',
                penwidth=2,
                sep='+10',
                esep='+10',
                splines='spline',
                style=('bold', 'filled', 'rounded'),
                truecolor=True,
                ),
            edge_attributes=dict(
                penwidth=2,
                ),
            node_attributes=dict(
                colorscheme='rdylbu9',
                penwidth=2,
                ),
            )
        for node in nodes:
            (
                artist_id,
                artist_name,
                cluster_id,
                distance,
                member_count,
                ) = node

            if not member_count:
                fontname = 'Arial'
                shape = 'box'
                style = ('bold', 'filled', 'rounded')
            else:
                fontname = 'Arial Bold'
                shape = 'circle'
                style = ('bold', 'filled')
            node = documentationtools.GraphvizNode(
                name='node{}'.format(artist_id),
                attributes=dict(
                    fillcolor=distance + 1,
                    fontname=fontname,
                    label=r'\n'.join(artist_name.split()),
                    shape=shape,
                    style=style,
                    ),
                )
            artist_id_to_node_mapping[artist_id] = node
            if cluster_id is not None:
                if cluster_id not in cluster_id_to_cluster_mapping:
                    cluster = documentationtools.GraphvizSubgraph(
                        is_cluster=False,
                        name='alias{}'.format(cluster_id)
                        )
                    cluster_id_to_cluster_mapping[cluster_id] = cluster
                    graphviz_graph.append(cluster)
                cluster = cluster_id_to_cluster_mapping[cluster_id]
                cluster.append(node)
            else:
                graphviz_graph.append(node)
        for head_id, tail_id, role in edges:
            head_node = artist_id_to_node_mapping[head_id]
            tail_node = artist_id_to_node_mapping[tail_id]
            if role == 'Alias':
                attributes = {
                    'dir': 'none',
                    'style': 'dotted',
                    }
            else:
                attributes = {}
            edge = documentationtools.GraphvizEdge(attributes=attributes)
            edge.attach(head_node, tail_node)
        root_node_names = ['node{}'.format(_.discogs_id) for _ in self.artists]
        for node in graphviz_graph:
            edge_count_weighting = len(node.edges)
            edge_count_weighting = math.sqrt(edge_count_weighting)
            node.attributes['fontsize'] = 12 + edge_count_weighting
            if node.name in root_node_names:
                node.attributes['fillcolor'] = 'black'
                node.attributes['fontcolor'] = 'white'
                node.attributes['fontsize'] = 20
        return graphviz_graph

    ### PUBLIC METHODS ###

    @staticmethod
    def get_neighborhood(artist, cache=None):
        key = 'cache:/api/artist/neighborhood/{}'.format(artist.discogs_id)
        if cache is not None:
            neighborhood = cache.get(key)
            if neighborhood is not None:
                #print('CACHE HIT: {}'.format(key))
                return neighborhood
            #print('CACHE MISS: {}'.format(key))
        as_dict = lambda x: {
            'id': x.discogs_id,
            'name': x.name,
            }
        aliases = []
        nodes = []
        edges = []
        for alias in artist.aliases:
            alias_query = models.Artist.objects(name=alias)
            if not alias_query.count():
                continue
            alias = alias_query.first()
            edge = sorted([artist.discogs_id, alias.discogs_id])
            edge.append('Alias')
            aliases.append(alias.discogs_id)
            edges.append(tuple(edge))
            nodes.append(as_dict(alias))
        for group in artist.groups:
            edge = (
                artist.discogs_id,
                group.discogs_id,
                'Member Of',
                )
            edges.append(edge)
            nodes.append(as_dict(group))
        for member in artist.members:
            edge = (
                member.discogs_id,
                artist.discogs_id,
                'Member Of',
                )
            edges.append(edge)
            nodes.append(as_dict(member))
        neighborhood = {
            'id': artist.discogs_id,
            'name': artist.name,
            'size': len(artist.members),
            'aliases': tuple(aliases),
            'nodes': tuple(sorted(nodes, key=lambda x: x['id'])),
            'edges': tuple(sorted(edges)),
            }
        if cache is not None:
            cache.set(key, neighborhood)
        return neighborhood

    def can_continue_searching(self, distance, artist_ids_visited):
        if (
            self.max_nodes and
            1 < distance and
            self.max_nodes <= len(artist_ids_visited)
            ):
            return False
        return True

    def collect_artists(self):
        artist_ids_visited = dict()
        artist_ids_to_visit = set(_.discogs_id for _ in self.artists)
        for distance in range(self.degree + 1):
            if not self.can_continue_searching(distance, artist_ids_visited):
                break
            current_artist_ids_to_visit = list(artist_ids_to_visit)
            artist_ids_to_visit.clear()
            while current_artist_ids_to_visit:
                if not self.can_continue_searching(distance, artist_ids_visited):
                    break
                artist_id = current_artist_ids_to_visit.pop()
                if artist_id in artist_ids_visited:
                    continue
                artist = models.Artist.objects.get(discogs_id=artist_id)
                neighborhood = self.get_neighborhood(artist, cache=self.cache)
                neighborhood['distance'] = distance
                artist_ids_visited[neighborhood['id']] = neighborhood
                for node in neighborhood['nodes']:
                    artist_ids_to_visit.add(node['id'])
        return artist_ids_visited

    def get_network(self):
        artists = self.collect_artists()
        edge_tuples = set()
        nodes = []
        cluster_count = 0
        cluster_map = {}
        for artist_id, artist_dict in sorted(artists.items()):
            incomplete = False
            for edge in artist_dict['edges']:
                if edge[0] in artists and edge[1] in artists:
                    edge_tuples.add(edge)
                else:
                    incomplete = True
            cluster = None
            if artist_dict['aliases']:
                if artist_dict['id'] not in cluster_map:
                    cluster_count += 1
                    cluster_map[artist_dict['id']] = cluster_count
                    for alias_id in artist_dict['aliases']:
                        cluster_map[alias_id] = cluster_count
                cluster = cluster_map[artist_dict['id']]
            node = {
                'distance': artist_dict['distance'],
                'group': cluster,
                'id': artist_dict['id'],
                'incomplete': incomplete,
                'name': artist_dict['name'],
                'size': artist_dict['size'],
                }
            nodes.append(node)
        edges = []
        for source, target, role in edge_tuples:
            edge = {'source': source, 'target': target, 'role': role}
            edges.append(edge)
        edges = tuple(sorted(edges, key=lambda x: (x['source'], x['target'])))
        nodes = tuple(sorted(nodes, key=lambda x: x['id']))
        network = {
            'center': [_.discogs_id for _ in self.artists],
            'nodes': nodes,
            'links': edges,
            }
        return network