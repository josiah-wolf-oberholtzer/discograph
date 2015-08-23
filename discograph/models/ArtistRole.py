import mongoengine
import re
from discograph.models.Model import Model


class ArtistRole(Model, mongoengine.EmbeddedDocument):

    ### CLASS VARIABLES ###

    _name_detail_pattern = re.compile('(.+)(\[.+\]\s*)+')
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
        in_bracket = False
        for character in element.text:
            if not in_bracket and character == '[':
                in_bracket = True
            elif in_bracket and character == ']':
                in_bracket = False
            elif not in_bracket and character == ',':
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
#        match = cls._name_detail_pattern.match(text)
#        if match is not None:
#            name, detail = match.groups()
#            name, detail = name.strip(), detail.strip()
#        else:
#            name, detail = text.strip(), None
        details = []
        index = 0
        match = cls._bracket_pattern.search(text, index)
        if match is not None:
            name = text[:match.start()].strip()
            while match is not None:
                details.extend(match.groups())
                match = cls._bracket_pattern.search(text, match.end())
        else:
            name = text
        detail = ', '.join(details) or None
        return cls(name=name, detail=detail)