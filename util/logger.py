import logging
from datetime import datetime
import shortuuid
from logging.handlers import TimedRotatingFileHandler

PROJECT_NAME = "TTS_API"
DEFAULT_LOGGER_FILENAME = f"log/tts_api.log"

default_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(filename)s | %(lineno)d | %(funcName)s | %(message)s'
)

class TestClass:
    def __init__(self) -> None:
        pass

def get_logger(level=logging.INFO, 
               name=PROJECT_NAME,
               cls=None, 
               file_name=DEFAULT_LOGGER_FILENAME,
               formatter=default_formatter,
               handlers=None):
    
    logger_name = "{} {}".format(name, cls.__class__.__name__) if cls else name
    logger = logging.getLogger(logger_name)
    logger.setLevel(level) if level else logger.setLevel(logging.INFO)

    _formatter = formatter
    _stream_handler = logging.StreamHandler()
    _stream_handler.setFormatter(_formatter)

    _file_handler = TimedRotatingFileHandler(filename=file_name, when="D", interval=1, backupCount=60)
    _file_handler.setFormatter(_formatter)

    logger.addHandler(_stream_handler)
    logger.addHandler(_file_handler)

    if handlers:
        for handler in handlers:
            logger.addHandler(handler)
    return logger

###################################### set logger ######################################
logger = get_logger(
    level=logging.DEBUG,
    name="TTS_API_LOGGER",
    file_name=DEFAULT_LOGGER_FILENAME,
)