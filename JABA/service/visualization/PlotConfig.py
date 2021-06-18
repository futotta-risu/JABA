class PlotConfig:
    def __init__(self,
                 indexType,
                 dataType,
                 indexFunction,
                 dataFunction,
                 index,
                 data,
                 args=None):
        self.indexType = indexType
        self.dataType = dataType
        self.indexFunction = indexFunction
        self.dataFunction = dataFunction

        self.index = index
        self.data = data

        self.args = args

    def getIndexType(self):
        return self.indexType

    def getDataType(self):
        return self.dataType

    def getIndexFunction(self):
        return self.indexFunction

    def getDataFunction(self):
        return self.dataFunction

    def getArgs(self):
        return self.args
