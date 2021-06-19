from service.visualization.types.maps.GenericMap import GenericMap


class SqrtMap(GenericMap):
    
    name = "Sqrt"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        data[variable] = data[variable] ** 0.5

        return data
