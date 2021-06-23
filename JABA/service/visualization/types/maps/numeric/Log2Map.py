from service.visualization.types.maps.GenericMap import GenericMap
import numpy as np

class Log2Map(GenericMap):
    
    name = "Log2"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        data[variable] = np.log2(data[variable])

        return data
