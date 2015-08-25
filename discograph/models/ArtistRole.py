import mongoengine
import re
from discograph.models.Model import Model


class ArtistRole(Model, mongoengine.EmbeddedDocument):

    ### CLASS VARIABLES ###

    _bracket_pattern = re.compile('\[(.+?)\]')

    ### MONGOENGINE FIELDS ###

    name = mongoengine.StringField()
    detail = mongoengine.StringField()

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        artist_roles = []
        if element is None or not element.text:
            return artist_roles
        current_text = ''
        bracket_depth = 0
        for character in element.text:
            if character == '[':
                bracket_depth += 1
            elif character == ']':
                bracket_depth -= 1
            elif not bracket_depth and character == ',':
                current_text = current_text.strip()
                if current_text:
                    artist_roles.append(cls.from_text(current_text))
                current_text = ''
                continue
            current_text += character
        current_text = current_text.strip()
        if current_text:
            artist_roles.append(cls.from_text(current_text))
        return artist_roles

    @classmethod
    def from_text(cls, text):
        name = ''
        current_buffer = ''
        details = []
        had_detail = False
        bracket_depth = 0
        for character in text:
            if character == '[':
                bracket_depth += 1
                if bracket_depth == 1 and not had_detail:
                    name = current_buffer
                    current_buffer = ''
                    had_detail = True
                elif 1 < bracket_depth:
                    current_buffer += character
            elif character == ']':
                bracket_depth -= 1
                if not bracket_depth:
                    details.append(current_buffer)
                    current_buffer = ''
                else:
                    current_buffer += character
            else:
                current_buffer += character
        if current_buffer and not had_detail:
            name = current_buffer
        name = name.strip()
        detail = ', '.join(_.strip() for _ in details)
        detail = detail or None
        return cls(name=name, detail=detail)