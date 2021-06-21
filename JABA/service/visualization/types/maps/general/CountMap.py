from service.visualization.types.maps.GenericMap import GenericMap


class CountMap(GenericMap):
    
    name = "Count"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        return data.count().reset_index(name="count")
