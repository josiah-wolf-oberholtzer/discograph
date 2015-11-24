import discograph
from abjad.tools import stringtools


class Test(discograph.DiscographTestCase):

    def test_01(self):
        entity = discograph.PostgresEntity.get(entity_type=1, entity_id=32550)
        roles = ['Alias', 'Member Of']
        relations = entity.structural_roles_to_relations(roles)
        relations = [v for k, v in sorted(relations.items())]
        actual = '\n'.join(repr(_) for _ in relations)
        expected = stringtools.normalize('''
            PostgresRelation(
                entity_one_id=100600,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=113965,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=152882,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=23446,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=241356,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=32550,
                entity_one_type=1,
                entity_two_id=2561672,
                entity_two_type=1,
                release_id=-1,
                role='Alias',
                year=-1
                )
            PostgresRelation(
                entity_one_id=354129,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=37806,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=409502,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=453969,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=53261,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            PostgresRelation(
                entity_one_id=55449,
                entity_one_type=1,
                entity_two_id=32550,
                entity_two_type=1,
                release_id=-1,
                role='Member Of',
                year=-1
                )
            ''')
        assert actual == expected
