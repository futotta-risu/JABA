from model.ScrapModel import ScrapModel

# TODO Change this with real factory


def createModelFrame(dtype):

    models = [
        model_class() for model_class in ScrapModel.__subclasses__()
        if model_class.name == dtype
    ]

    if not models:
        raise NotImplementedError()

    return models[0].createModelFrame()
