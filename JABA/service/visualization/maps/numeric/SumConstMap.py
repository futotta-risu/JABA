from service.visualization.maps.GenericMap import GenericMap


class SumConstMap(GenericMap):

    name = "Constant Sum"

    def __init__(self, attrs):
        if attrs is None:
            attrs = {"val": "1"}

        if "val" not in attrs:
            attrs["val"] = "1"

        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]
        val = self.getAttrs()["val"]

        data[variable] = data[variable] + int(val)

        return data

    def getAttrsWithTypes(self):
        return {"val": ("Text", "1")}
