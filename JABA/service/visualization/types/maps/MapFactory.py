from service.visualization.types.maps.general.CountMap import CountMap

class MapFactory:
    
    def apply(self, dtype, frame, args = None):
        if dtype == "count":
            fmap = CountMap(args)
        else:
            raise NotImplementedError()
        
        return fmap.apply(frame)