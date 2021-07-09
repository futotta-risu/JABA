from pyqtgraph import plot
from pyqtgraph import PlotWidget

class PlotService:
    def __init__(self):
        self.resetID()

    def resetID(self):
        self.id = 1

    def getPlotID(self):
        self.id += 1
        return self.id


    def applyPlotMaps(self, data, plotConfig):
        ''' Apply plot maps to the data '''
        
        for fmap in plotConfig.map_list:
            data = fmap.apply(data)
        
        if plotConfig.index == "Range Index":
            return range(1, len(data)+1), data[plotConfig.data]
        else:
            return data[plotConfig.index], data[plotConfig.data]
