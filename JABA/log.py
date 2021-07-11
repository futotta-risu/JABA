from loguru import logger


def start_log():

    log_format = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

    logger.add(
        "file_{time}.log", format=log_format, level="DEBUG",
        rotation="5 MB", retention="10 days", compression="zip",
        backtrace=True, diagnose=True
    )
