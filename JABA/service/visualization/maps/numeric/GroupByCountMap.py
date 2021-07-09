from service.visualization.maps.GenericMap import GenericMap


class GroupByCountMap(GenericMap):
    
    name = "Group Count"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        return data.groupby(variable, as_index=False).count()
