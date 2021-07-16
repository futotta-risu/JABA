from service.visualization.maps.GenericMap import GenericMap


class MultiplyMap(GenericMap):

    name = "Multiply"

    def __init__(self, attrs):
        if attrs is None:
            attrs = {"second": None}

        if "second" not in attrs:
            attrs["second"] = None

        super().__init__(attrs)

    def apply(self, data):
        attrs = self.getAttrs()

        if attrs["second"] is None:
            raise Exception()

        variable = attrs["variable"]
        second = attrs["second"]

        data[variable + "*" + second] = data[variable] * data[second]

        return data

    def getAttrsWithTypes(self):
        return {"second": ("Variable", "")}
