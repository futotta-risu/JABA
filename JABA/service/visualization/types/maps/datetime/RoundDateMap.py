from service.visualization.types.maps.GenericMap import GenericMap


class RoundDateMap(GenericMap):
    
    def __init__(self, attrs):
        super().__init__("RoundDate", attrs)
    
    def apply(self, data):
        variable = self.getAttrs()['variable']
        round = self.getAttrs()['round']
        
        data['round_' + variable] = data[variable].round(round)
        
        return data
    