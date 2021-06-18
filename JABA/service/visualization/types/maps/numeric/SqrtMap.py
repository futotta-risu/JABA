from service.visualization.types.maps.GenericMap import GenericMap


class SqrtMap(GenericMap):

    def __init__(self, attrs):
        super().__init__("Sqrt", attrs)

    def apply(self, data):
        variable = self.getAttrs()['variable']

        data[variable] = data[variable] ** 0.5

        return data
