from service.visualization.maps.GenericMap import GenericMap


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
