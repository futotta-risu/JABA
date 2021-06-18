# To load classes in memory to be available to use, import them
from service.visualization.types.maps.datetime.RoundDateMap import RoundDateMap
from service.visualization.types.maps.general.CountMap import CountMap
from service.visualization.types.maps.GenericMap import GenericMap
from service.visualization.types.maps.numeric.GroupByCountMap import \
    GroupByCountMap
from service.visualization.types.maps.numeric.GroupByMeanMap import \
    GroupByMeanMap
from service.visualization.types.maps.numeric.SqrtMap import SqrtMap


class MapFactory:
    def getMapList(self):
        return [q.__name__ for q in GenericMap.__subclasses__()]

    def __get_map(self, dtype, args=None):
        map_list = [
            map_class(args) for map_class in GenericMap.__subclasses__()
            if map_class.__name__ == dtype
        ]

        if not map_list:
            raise NotImplementedError()

        return map_list[0]

    def getAttrsWithTypes(self, dtype):
        fmap = self.__get_map(dtype)
        return fmap.getAttrsWithTypes()

    def apply(self, dtype, frame, args=None):

        fmap = self.__get_map(dtype, args)

        return fmap.apply(frame), fmap
