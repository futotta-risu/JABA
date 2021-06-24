from service.visualization.types.maps.GenericMap import GenericMap


class RoundDateMap(GenericMap):
    
    name = "Round Date"
    def __init__(self, attrs):
        if attrs is None:
            attrs = {"round":"min"}
            
        if "round" not in attrs:
            attrs["round"] = "min"
            
        super().__init__(attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]
        round = self.getAttrs()["round"]

        data["round_" + variable] = data[variable].dt.floor(round)

        return data

    def getAttrsWithTypes(self):
        return {"round": ("Text", "min")}
