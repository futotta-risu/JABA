from service.visualization.maps.GenericMap import GenericMap
import numpy as np

class LogMap(GenericMap):
    
    name = "Log"
    
    def __init__(self, attrs):
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]

        data[variable] = np.log(data[variable])

        return data
