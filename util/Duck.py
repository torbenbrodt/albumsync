class Duck:
    def __init__(self):
        pass

    @staticmethod
    def create(dic={}):
        return type('lamdbaobject', (object,), dic)()