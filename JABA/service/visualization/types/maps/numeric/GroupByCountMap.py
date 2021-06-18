from service.visualization.types.maps.GenericMap import GenericMap


class GroupByCountMap(GenericMap):
    def __init__(self, attrs):
        super().__init__("GroupByCount", attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        return data.groupby(variable, as_index=False).count()
