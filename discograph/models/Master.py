import mongoengine


class Master(mongoengine.Document):

    ### PUBLIC METHODS ###

    @classmethod
    def from_element(cls, element):
        pass
