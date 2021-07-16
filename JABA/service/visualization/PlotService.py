from service.scraper.ScrapService import ScrapService

import pyqtgraph as pg


class PlotService:
    def __init__(self):
        self.resetID()

    def resetID(self):
        self.id = 1

    def getPlotID(self):
        self.id += 1
        return self.id

    def getDataPriorities(self, name):
        ''' Temporary function for data prioritation. Sentiment -> Tweet. Bitcoin. '''

        # TODO Refactor this code
        if name == "Sentiment":
            return 0
        elif name == "Bitcoin":
            return 2
        else:
            return 1

    def reorderConfiguration(self, configurations):
        types = [[], [], []]
        for config in configurations:
            types[self.getDataPriorities(config['config'].variable_type)] += [config]

        configurations = [j for i in types for j in i]
        return configurations

    def updatePlots(self, configurations, date, algorithm):
        '''
            Updates the plots.
        '''

        configurations = self.reorderConfiguration(configurations)

        pre_type, pre_data = -1, None
        scrapService = ScrapService()
        for config in configurations:
            pConfig, widget = config["config"], config["widget"]
            act_type = self.getDataPriorities(pConfig.variable_type)

            args = {"date": date, "algorithm": algorithm}

            if(pre_type != act_type and not (pre_type == 0 and act_type == 1)):
                pre_type = act_type
                pre_data = scrapService.get_data_by_category(pConfig.variable_type, args)

            index, data = self.applyPlotMaps(pre_data, pConfig)

            widget.clear()
            widget.plot(index, data, pen=pg.mkPen('18BEBE', width=1))

    def applyPlotMaps(self, data, plotConfig):
        ''' Apply plot maps to the data '''

        for fmap in plotConfig.map_list:
            data = fmap.apply(data)

        if plotConfig.index == "Range Index":
            return range(1, len(data) + 1), data[plotConfig.data]
        else:
            return data[plotConfig.index], data[plotConfig.data]
