from service.visualization.maps.GenericMap import GenericMap


class PCTChangeMap(GenericMap):
    
    name = "Percentage Change"
    
    def __init__(self, attrs):
        super().__init__(attrs)
        
        

    def apply(self, data):
            
        variable = self.getAttrs()["variable"]

        data[variable + "_PCT"] = data[variable].pct_change()

        return data