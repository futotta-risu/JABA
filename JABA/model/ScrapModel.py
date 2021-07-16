class ScrapModel:
    '''
        Scrap model base for other models.
    '''

    name = ""
    column_names = None

    def setModelTypes(self, df):
        ''' Updates the model data types '''
        pass

    def createModelFrame(self):
        ''' Creates a model with the desired columns and types '''
        pass
