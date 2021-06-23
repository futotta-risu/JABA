class ScrapModel:
    '''
        Scrap model base for other models.
    '''
    
    name = ""
    column_names = None

    def setModelTypes(self, df):
        pass

    def createModelFrame(self):
        pass