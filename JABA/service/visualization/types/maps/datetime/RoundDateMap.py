from service.visualization.types.maps.GenericMap import GenericMap


class RoundDateMap(GenericMap):
    def __init__(self, attrs):
        
        if attrs == None:
            attrs = {"round":"min"}
            
        if not "round" in attrs:
            attrs["round"] = "min"
            
            
            
        super().__init__("RoundDate", attrs)

    def apply(self, data):
        variable = self.getAttrs()["variable"]
        round = self.getAttrs()["round"]

        data["round_" + variable] = data[variable].floor(round)

        return data

    def getAttrsWithTypes(self):
        return {"round": ("Text", "min")}
