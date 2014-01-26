from service.abstract.AbstractMedia import AbstractMedia


class Media(AbstractMedia):
    """Facebook Media"""

    def __init__(self, album, path):
        AbstractMedia.__init__(self, album, path)
