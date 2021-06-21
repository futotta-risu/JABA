from service.visualization.types.maps.GenericMap import GenericMap


class MultiplyMap(GenericMap):
    
    name = "Multiply"
    
    def __init__(self, attrs):
        if attrs == None:
            attrs = {"second":None}
            
        if not "second" in attrs:
            attrs["second"] = None
            
        super().__init__(attrs)
        
        

    def apply(self, data):
        attrs = self.getAttrs()
        
        if attrs["second"] == None:
            raise Exception()
            
        variable = attrs["variable"]
        second = attrs["second"]

        data[variable + "*" + second] = data[variable] * data[second]

        return data
    
    def getAttrsWithTypes(self):
        return {"second": ("Variable", "")}