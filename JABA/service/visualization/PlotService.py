from pyqtgraph import plot
from pyqtgraph import PlotWidget

from .PlotConfig import PlotConfig


class PlotService:
    def __init__(self):
        self.resetID()
        pass

    def resetID(self):
        self.id = 1

    def getPlotID(self):
        self.id += 1
        return self.id

    def createPlotConfig(self,
                         indexType,
                         dataType,
                         indexFunction,
                         dataFunction,
                         args=None):
        """
        Returns id and plot widget and config dict.
        """
        plotConfig = PlotConfig(indexType, dataType, indexFunction,
                                dataFunction, args)
        widget = PlotWidget()

        return self.getPlotID(), plotConfig, widget

    def prepareData(self, data, plotConfig):

        dataFunction = plotConfig.getDataFunction()
        return_index, return_data = data.index, data
        dataKey = "data"

        if plotConfig.getIndexFunction() == "round":
            round_var = plotConfig.getArgs()["round_var"]
            data["round_time"] = data["Datetime"].round(round_var)

            data = data.groupby("round_time").agg({"round_time": dataFunction})
            return_index = list(range(0, len(data.index)))
            return_data = data["round_time"].to_list()

        return return_index, return_data

    def applyPlotMaps(self, data, plotConfig):

        for fmap in plotConfig.map_list:
            data = fmap.apply(data)
        
        if plotConfig.index == "Range Index":
            return range(1, len(data)+1), data[plotConfig.data]
        else:
            return data[plotConfig.index], data[plotConfig.data]
