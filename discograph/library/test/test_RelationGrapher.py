# -*- coding: utf-8 -*-
import discograph
import json
from abjad import stringtools


class Test(discograph.DiscographTestCase):
    """
    Problematic networks:

        - 296570: 306 nodes, 13688 links, 5 pages: 149, 4, 4, 4, 158
        - 1946151: unbalanced paging
        - 491160: bifurcated dense alias networks

    """

    json_kwargs = {
        'indent': 4,
        'separators': (',', ': '),
        'sort_keys': True,
        }

    def test___call___01(self):
        artist = discograph.PostgresEntity.get(entity_type=1, name='Morris Day')
        roles = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=1,
            roles=roles,
            )
        network = grapher.__call__()
        actual = json.dumps(network, **self.json_kwargs)
        expected = stringtools.normalize('''
            {
                "center": {
                    "key": "artist-152882", 
                    "name": "Morris Day"
                },
                "links": [
                    {
                        "key": "artist-152882-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-152882-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-32550-alias-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Alias",
                        "source": "artist-32550",
                        "target": "artist-2561672"
                    }
                ],
                "nodes": [
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 32550,
                        "key": "artist-32550",
                        "links": [
                            "artist-152882-member-of-artist-32550",
                            "artist-32550-alias-artist-2561672"
                        ],
                        "missing": 10,
                        "name": "The Time",
                        "pages": [
                            1
                        ],
                        "size": 11,
                        "type": "artist"
                    },
                    {
                        "distance": 0,
                        "id": 152882,
                        "key": "artist-152882",
                        "links": [
                            "artist-152882-member-of-artist-2561672",
                            "artist-152882-member-of-artist-32550"
                        ],
                        "missing": 0,
                        "name": "Morris Day",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 2561672,
                        "key": "artist-2561672",
                        "links": [
                            "artist-152882-member-of-artist-2561672",
                            "artist-32550-alias-artist-2561672"
                        ],
                        "missing": 6,
                        "name": "The Original 7ven",
                        "pages": [
                            1
                        ],
                        "size": 7,
                        "type": "artist"
                    }
                ],
                "pages": 1
            }
        ''')
        assert actual == expected

    def test___call___02(self):
        artist = discograph.PostgresEntity.get(entity_type=1, name='Morris Day')
        roles = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            max_nodes=5,
            roles=roles,
            )
        network = grapher.__call__()
        actual = json.dumps(network, **self.json_kwargs)
        expected = stringtools.normalize('''
            {
                "center": {
                    "key": "artist-152882",
                    "name": "Morris Day"
                },
                "links": [
                    {
                        "key": "artist-100600-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-100600",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-100600-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-100600",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-113965-member-of-artist-2561672",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-113965",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-113965-member-of-artist-32550",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-113965",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-152882-member-of-artist-2561672",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-152882-member-of-artist-32550",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-23446-member-of-artist-32550",
                        "pages": [
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-23446",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-241356-member-of-artist-2561672",
                        "pages": [
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-241356",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-241356-member-of-artist-32550",
                        "pages": [
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-241356",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-242702-member-of-artist-32550",
                        "pages": [
                            3
                        ],
                        "role": "Member Of",
                        "source": "artist-242702",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-32550-alias-artist-2561672",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "role": "Alias",
                        "source": "artist-32550",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-354129-member-of-artist-2561672",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-354129",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-354129-member-of-artist-32550",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-354129",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-37806-member-of-artist-2561672",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-37806",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-37806-member-of-artist-32550",
                        "pages": [
                            2
                        ],
                        "role": "Member Of",
                        "source": "artist-37806",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-409502-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-409502",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-453969-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-453969",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-55449-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-55449",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-55449-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-55449",
                        "target": "artist-32550"
                    }
                ],
                "nodes": [
                    {
                        "distance": 2,
                        "id": 23446,
                        "key": "artist-23446",
                        "links": [
                            "artist-23446-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Alexander O'Neal",
                        "pages": [
                            3
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 32550,
                        "key": "artist-32550",
                        "links": [
                            "artist-100600-member-of-artist-32550",
                            "artist-113965-member-of-artist-32550",
                            "artist-152882-member-of-artist-32550",
                            "artist-23446-member-of-artist-32550",
                            "artist-241356-member-of-artist-32550",
                            "artist-242702-member-of-artist-32550",
                            "artist-32550-alias-artist-2561672",
                            "artist-354129-member-of-artist-32550",
                            "artist-37806-member-of-artist-32550",
                            "artist-409502-member-of-artist-32550",
                            "artist-453969-member-of-artist-32550",
                            "artist-55449-member-of-artist-32550"
                        ],
                        "missing": 0,
                        "missingByPage": {
                            "1": 6,
                            "2": 7,
                            "3": 7
                        },
                        "name": "The Time",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "size": 11,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 37806,
                        "key": "artist-37806",
                        "links": [
                            "artist-37806-member-of-artist-2561672",
                            "artist-37806-member-of-artist-32550"
                        ],
                        "missing": 2,
                        "name": "Jesse Johnson",
                        "pages": [
                            2
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 55449,
                        "key": "artist-55449",
                        "links": [
                            "artist-55449-member-of-artist-2561672",
                            "artist-55449-member-of-artist-32550"
                        ],
                        "missing": 3,
                        "name": "Terry Lewis",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 100600,
                        "key": "artist-100600",
                        "links": [
                            "artist-100600-member-of-artist-2561672",
                            "artist-100600-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Monte Moir",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 113965,
                        "key": "artist-113965",
                        "links": [
                            "artist-113965-member-of-artist-2561672",
                            "artist-113965-member-of-artist-32550"
                        ],
                        "missing": 4,
                        "name": "Jellybean Johnson",
                        "pages": [
                            2
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 0,
                        "id": 152882,
                        "key": "artist-152882",
                        "links": [
                            "artist-152882-member-of-artist-2561672",
                            "artist-152882-member-of-artist-32550"
                        ],
                        "missing": 0,
                        "name": "Morris Day",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 2,
                        "distance": 2,
                        "id": 241356,
                        "key": "artist-241356",
                        "links": [
                            "artist-241356-member-of-artist-2561672",
                            "artist-241356-member-of-artist-32550"
                        ],
                        "missing": 4,
                        "name": "James Harris III",
                        "pages": [
                            3
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 3,
                        "distance": 2,
                        "id": 242702,
                        "key": "artist-242702",
                        "links": [
                            "artist-242702-member-of-artist-32550"
                        ],
                        "missing": 5,
                        "name": "Paul Peterson",
                        "pages": [
                            3
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 354129,
                        "key": "artist-354129",
                        "links": [
                            "artist-354129-member-of-artist-2561672",
                            "artist-354129-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Jerome Benton",
                        "pages": [
                            2
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 409502,
                        "key": "artist-409502",
                        "links": [
                            "artist-409502-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Mark Cardenas",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 453969,
                        "key": "artist-453969",
                        "links": [
                            "artist-453969-member-of-artist-32550"
                        ],
                        "missing": 2,
                        "name": "Jerry Hubbard",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 2561672,
                        "key": "artist-2561672",
                        "links": [
                            "artist-100600-member-of-artist-2561672",
                            "artist-113965-member-of-artist-2561672",
                            "artist-152882-member-of-artist-2561672",
                            "artist-241356-member-of-artist-2561672",
                            "artist-32550-alias-artist-2561672",
                            "artist-354129-member-of-artist-2561672",
                            "artist-37806-member-of-artist-2561672",
                            "artist-55449-member-of-artist-2561672"
                        ],
                        "missing": 0,
                        "missingByPage": {
                            "1": 4,
                            "2": 3,
                            "3": 5
                        },
                        "name": "The Original 7ven",
                        "pages": [
                            1,
                            2,
                            3
                        ],
                        "size": 7,
                        "type": "artist"
                    }
                ],
                "pages": 3
            }
        ''')
        assert actual == expected

    def test___call___03(self):
        artist = discograph.PostgresEntity.get(entity_type=1, name='Morris Day')
        roles = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            link_ratio=2,
            roles=roles,
            )
        network = grapher.__call__()
        actual = json.dumps(network, **self.json_kwargs)
        expected = stringtools.normalize('''
            {
                "center": {
                    "key": "artist-152882",
                    "name": "Morris Day"
                },
                "links": [
                    {
                        "key": "artist-100600-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-100600",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-100600-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-100600",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-113965-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-113965",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-113965-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-113965",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-152882-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-152882-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-152882",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-23446-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-23446",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-241356-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-241356",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-241356-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-241356",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-242702-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-242702",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-32550-alias-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Alias",
                        "source": "artist-32550",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-354129-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-354129",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-354129-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-354129",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-37806-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-37806",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-37806-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-37806",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-409502-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-409502",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-453969-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-453969",
                        "target": "artist-32550"
                    },
                    {
                        "key": "artist-55449-member-of-artist-2561672",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-55449",
                        "target": "artist-2561672"
                    },
                    {
                        "key": "artist-55449-member-of-artist-32550",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-55449",
                        "target": "artist-32550"
                    }
                ],
                "nodes": [
                    {
                        "distance": 2,
                        "id": 23446,
                        "key": "artist-23446",
                        "links": [
                            "artist-23446-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Alexander O'Neal",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 32550,
                        "key": "artist-32550",
                        "links": [
                            "artist-100600-member-of-artist-32550",
                            "artist-113965-member-of-artist-32550",
                            "artist-152882-member-of-artist-32550",
                            "artist-23446-member-of-artist-32550",
                            "artist-241356-member-of-artist-32550",
                            "artist-242702-member-of-artist-32550",
                            "artist-32550-alias-artist-2561672",
                            "artist-354129-member-of-artist-32550",
                            "artist-37806-member-of-artist-32550",
                            "artist-409502-member-of-artist-32550",
                            "artist-453969-member-of-artist-32550",
                            "artist-55449-member-of-artist-32550"
                        ],
                        "missing": 0,
                        "name": "The Time",
                        "pages": [
                            1
                        ],
                        "size": 11,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 37806,
                        "key": "artist-37806",
                        "links": [
                            "artist-37806-member-of-artist-2561672",
                            "artist-37806-member-of-artist-32550"
                        ],
                        "missing": 2,
                        "name": "Jesse Johnson",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 55449,
                        "key": "artist-55449",
                        "links": [
                            "artist-55449-member-of-artist-2561672",
                            "artist-55449-member-of-artist-32550"
                        ],
                        "missing": 3,
                        "name": "Terry Lewis",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 100600,
                        "key": "artist-100600",
                        "links": [
                            "artist-100600-member-of-artist-2561672",
                            "artist-100600-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Monte Moir",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 113965,
                        "key": "artist-113965",
                        "links": [
                            "artist-113965-member-of-artist-2561672",
                            "artist-113965-member-of-artist-32550"
                        ],
                        "missing": 4,
                        "name": "Jellybean Johnson",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 0,
                        "id": 152882,
                        "key": "artist-152882",
                        "links": [
                            "artist-152882-member-of-artist-2561672",
                            "artist-152882-member-of-artist-32550"
                        ],
                        "missing": 0,
                        "name": "Morris Day",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 2,
                        "distance": 2,
                        "id": 241356,
                        "key": "artist-241356",
                        "links": [
                            "artist-241356-member-of-artist-2561672",
                            "artist-241356-member-of-artist-32550"
                        ],
                        "missing": 4,
                        "name": "James Harris III",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 3,
                        "distance": 2,
                        "id": 242702,
                        "key": "artist-242702",
                        "links": [
                            "artist-242702-member-of-artist-32550"
                        ],
                        "missing": 5,
                        "name": "Paul Peterson",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 354129,
                        "key": "artist-354129",
                        "links": [
                            "artist-354129-member-of-artist-2561672",
                            "artist-354129-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Jerome Benton",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 409502,
                        "key": "artist-409502",
                        "links": [
                            "artist-409502-member-of-artist-32550"
                        ],
                        "missing": 1,
                        "name": "Mark Cardenas",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 2,
                        "id": 453969,
                        "key": "artist-453969",
                        "links": [
                            "artist-453969-member-of-artist-32550"
                        ],
                        "missing": 2,
                        "name": "Jerry Hubbard",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 2561672,
                        "key": "artist-2561672",
                        "links": [
                            "artist-100600-member-of-artist-2561672",
                            "artist-113965-member-of-artist-2561672",
                            "artist-152882-member-of-artist-2561672",
                            "artist-241356-member-of-artist-2561672",
                            "artist-32550-alias-artist-2561672",
                            "artist-354129-member-of-artist-2561672",
                            "artist-37806-member-of-artist-2561672",
                            "artist-55449-member-of-artist-2561672"
                        ],
                        "missing": 0,
                        "name": "The Original 7ven",
                        "pages": [
                            1
                        ],
                        "size": 7,
                        "type": "artist"
                    }
                ],
                "pages": 1
            }
        ''')
        assert actual == expected

    def test___call___04(self):
        r'''Missing count takes into account structural roles: members,
        aliases, groups, sublabels, parent labels, etc.
        '''
        artist = discograph.PostgresEntity.get(
            entity_type=1, 
            entity_id=1362698,
            )
        roles = ['Alias', 'Member Of']
        grapher = discograph.RelationGrapher(
            artist,
            degree=12,
            roles=roles,
            )
        network = grapher.__call__()
        actual = json.dumps(network, **self.json_kwargs)
        expected = stringtools.normalize('''
            {
                "center": {
                    "key": "artist-1362698",
                    "name": "Revolution (13)"
                },
                "links": [
                    {
                        "key": "artist-144943-alias-artist-535046",
                        "pages": [
                            1
                        ],
                        "role": "Alias",
                        "source": "artist-144943",
                        "target": "artist-535046"
                    },
                    {
                        "key": "artist-144943-member-of-artist-1362698",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-144943",
                        "target": "artist-1362698"
                    },
                    {
                        "key": "artist-271585-member-of-artist-1362698",
                        "pages": [
                            1
                        ],
                        "role": "Member Of",
                        "source": "artist-271585",
                        "target": "artist-1362698"
                    }
                ],
                "nodes": [
                    {
                        "cluster": 1,
                        "distance": 1,
                        "id": 144943,
                        "key": "artist-144943",
                        "links": [
                            "artist-144943-alias-artist-535046",
                            "artist-144943-member-of-artist-1362698"
                        ],
                        "missing": 0,
                        "name": "DJ D-Sfase",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 1,
                        "id": 271585,
                        "key": "artist-271585",
                        "links": [
                            "artist-271585-member-of-artist-1362698"
                        ],
                        "missing": 0,
                        "name": "Neuroti-k",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "cluster": 1,
                        "distance": 2,
                        "id": 535046,
                        "key": "artist-535046",
                        "links": [
                            "artist-144943-alias-artist-535046"
                        ],
                        "missing": 0,
                        "name": "Jose Antonio Gonzalez Sanchez",
                        "pages": [
                            1
                        ],
                        "size": 0,
                        "type": "artist"
                    },
                    {
                        "distance": 0,
                        "id": 1362698,
                        "key": "artist-1362698",
                        "links": [
                            "artist-144943-member-of-artist-1362698",
                            "artist-271585-member-of-artist-1362698"
                        ],
                        "missing": 0,
                        "name": "Revolution (13)",
                        "pages": [
                            1
                        ],
                        "size": 2,
                        "type": "artist"
                    }
                ],
                "pages": 1
            }
        ''')
        assert actual == expected

    def test___call___05(self):
        artist = discograph.PostgresEntity.get(
            entity_type=2, 
            name='Computer Hell Cabin',
            )
        roles = ['Recorded At']
        grapher = discograph.RelationGrapher(
            artist,
            degree=2,
            roles=roles,
            )
        network = grapher.__call__()  # Should not error.
