from service.visualization.types.maps.GenericMap import GenericMap


class CountMap(GenericMap):

    def __init__(self, attrs):
        super().__init__("Count", attrs)

    def apply(self, data):
        return data.count().reset_index(name="count")
