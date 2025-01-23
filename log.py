import logging

def initialize():
    formatter = logging.Formatter("[Line: %(lineno)d | File: %(filename)s | Func: %(funcName)s] [%(asctime)s] [%(levelname)s]: %(message)s")
    handler = logging.FileHandler("output.log")
    handler.setFormatter(formatter)

    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
