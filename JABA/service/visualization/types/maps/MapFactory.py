# To load classes in memory to be available to use, import them
from service.visualization.types.maps.datetime.RoundDateMap import RoundDateMap
from service.visualization.types.maps.general.CountMap import CountMap
from service.visualization.types.maps.GenericMap import GenericMap
from service.visualization.types.maps.numeric.GroupByCountMap import \
    GroupByCountMap
from service.visualization.types.maps.numeric.GroupByMeanMap import \
    GroupByMeanMap
from service.visualization.types.maps.numeric.GroupBySumMap import \
    GroupBySumMap
from service.visualization.types.maps.numeric.SqrtMap import SqrtMap
from service.visualization.types.maps.numeric.SumConstMap import SumConstMap
from service.visualization.types.maps.numeric.LogMap import LogMap
from service.visualization.types.maps.numeric.Log2Map import Log2Map
from service.visualization.types.maps.numeric.MultiplyMap import MultiplyMap
from service.visualization.types.maps.numeric.PCTChangeMap import PCTChangeMap

class MapFactory:
    def getMapList(self):
        return [q for q in GenericMap.__subclasses__()]
    
    def __get_map(self, dtype, args=None):
        map_list = [
            map_class(args) for map_class in GenericMap.__subclasses__()
            if map_class.__name__ == dtype
        ]

        if not map_list:
            raise NotImplementedError()

        return map_list[0]

    def getAttrsWithTypes(self, dtype):
        return self.__get_map(dtype).getAttrsWithTypes()

    def apply(self, dtype, frame, args=None):

        fmap = self.__get_map(dtype, args)

        return fmap.apply(frame), fmap
