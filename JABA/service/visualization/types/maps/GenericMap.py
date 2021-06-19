class GenericMap:
    """
    Interface for Mapping functions
    """
    def __init__(self, name, attrs):
        self.attrs = attrs
        self.name = name

    def apply(self, data):
        raise NotImplementedError()

    def getName(self):
        return self.name

    def getAttrs(self):
        return self.attrs

    def getAttrsWithTypes(self):
        return {}

    def setAttrs(self, attrs: dict):
        self.attrs = attrs
