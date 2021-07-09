class GenericMap:
    """
    Interface for Mapping functions
    """

    name = "Generic Map"

    def __init__(self, attrs):
        self.attrs = attrs

    def apply(self, data):
        raise NotImplementedError()

    @classmethod
    def getName(cls):
        return cls.name

    def getAttrs(self):
        return self.attrs

    def getAttrsWithTypes(self):
        return {}

    def setAttrs(self, attrs: dict):
        self.attrs = attrs
