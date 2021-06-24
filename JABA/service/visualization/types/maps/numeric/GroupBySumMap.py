from service.visualization.types.maps.GenericMap import GenericMap


class GroupBySumMap(GenericMap):
    
    name = "Group Sum"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        return data.groupby(variable, as_index=False).sum()
