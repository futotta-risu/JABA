from service.visualization.types.maps.general.CountMap import CountMap
from service.visualization.types.maps.numeric.SqrtMap import SqrtMap

from service.visualization.types.maps.GenericMap import GenericMap

class MapFactory:
    
    def getMapList(self):
        return [ q.__name__ for q in GenericMap.__subclasses__()]
    
    def apply(self, dtype, frame, args = None):
        map_list = [map_class(args) for map_class in GenericMap.__subclasses__() if map_class.__name__ == dtype]
        
        if not map_list:
            raise NotImplementedError()
            
        fmap = map_list[0]
        
        return fmap.apply(frame), fmap