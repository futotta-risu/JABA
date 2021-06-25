from service.visualization.types.maps.GenericMap import GenericMap


class GroupByMeanMap(GenericMap):
    
    name = "Group Mean"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        return data.groupby(variable, as_index=False).mean()
