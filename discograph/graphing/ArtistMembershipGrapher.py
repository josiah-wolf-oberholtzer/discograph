import math
from abjad import documentationtools
from discograph import models


class ArtistMembershipGrapher(object):

    ### INITIALIZER ###

    def __init__(self, artist, degree):
        assert isinstance(artist, models.Artist)
        assert 0 < degree
        self.artist = artist
        self.degree = degree

    ### SPECIAL METHODS ###

    def __graph__(self):
        artist_ids, artist_id_edges = self.discover_artist_membership()
        artist_id_to_node_mapping = {}
        graphviz_graph = documentationtools.GraphvizGraph(
            attributes=dict(
                bgcolor='transparent',
                color='lightslategrey',
                fontname='Arial',
                output_order='edgesfirst',
                overlap='prism',
                penwidth=2,
                root='node{}'.format(self.artist.discogs_id),
                splines='spline',
                style=('dotted', 'rounded'),
                truecolor=True,
                ),
            edge_attributes=dict(
                penwidth=2,
                ),
            node_attributes=dict(
                colorscheme='pastel19',
                penwidth=2,
                ),
            )
        for i, artist_id in enumerate(artist_ids):
            artist = models.Artist.objects.get(discogs_id=artist_id)
            if not artist.members:
                fontname = 'Arial'
                shape = 'box'
                style = ('bold', 'filled', 'rounded')
            else:
                fontname = 'Arial Bold'
                shape = 'circle'
                style = ('bold', 'filled')
            node = documentationtools.GraphvizNode(
                name='node{}'.format(artist.discogs_id),
                attributes=dict(
                    fillcolor=i % 9 + 1,
                    fontname=fontname,
                    label=r'\n'.join(artist.name.split()),
                    shape=shape,
                    style=style,
                    ),
                )
            artist_id_to_node_mapping[artist_id] = node
            graphviz_graph.append(node)
        for head_id, tail_id in artist_id_edges:
            head_node = artist_id_to_node_mapping[head_id]
            tail_node = artist_id_to_node_mapping[tail_id]
            edge = documentationtools.GraphvizEdge()
            edge.attach(head_node, tail_node)
        for node in graphviz_graph:
            edge_count_weighting = len(node.edges)
            edge_count_weighting = math.sqrt(edge_count_weighting)
            node.attributes['fontsize'] = 12 + edge_count_weighting
            if node.name == 'node{}'.format(self.artist.discogs_id):
                node.attributes['fillcolor'] = 'black'
                node.attributes['fontcolor'] = 'white'
                node.attributes['fontsize'] = 20
        return graphviz_graph

    ### PUBLIC METHODS ###

    def discover_artist_membership(self):
        edges = set()
        artist_ids_visited = set()
        artist_ids_to_visit = set([self.artist.discogs_id])
        for i in range(self.degree + 1):
            current_artist_ids_to_visit = list(artist_ids_to_visit)
            artist_ids_to_visit.clear()
            while current_artist_ids_to_visit:
                artist_id = current_artist_ids_to_visit.pop()
                if artist_id in artist_ids_visited:
                    continue
                artist = models.Artist.objects.get(discogs_id=artist_id)
                for group in artist.groups:
                    if i < self.degree:
                        artist_ids_to_visit.add(group.discogs_id)
                        edge = (artist.discogs_id, group.discogs_id)
                        edges.add(edge)
                for member in artist.members:
                    if i < self.degree:
                        artist_ids_to_visit.add(member.discogs_id)
                        edge = (member.discogs_id, artist.discogs_id)
                        edges.add(edge)
                artist_ids_visited.add(artist_id)
            message = 'DEGREE {}: {} artists, {} edges'.format(
                i,
                len(artist_ids_visited),
                len(edges),
                )
            print(message)
        for head, tail in edges:
            assert head in artist_ids_visited
            assert tail in artist_ids_visited
        return artist_ids_visited, edges