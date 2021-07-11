from model.ScrapModel import ScrapModel

from loguru import logger
# TODO Change this with real factory


def createModelFrame(dtype):

    models = [
        model_class() for model_class in ScrapModel.__subclasses__()
        if model_class.name == dtype
    ]

    if not models:
        logger.error(f"Error trying to create a model of type {dtype}")
        raise NotImplementedError()

    return models[0].createModelFrame()
