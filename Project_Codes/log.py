from config import logging


log_file = "./logfile.log"
# filemode has to be adjusted
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger("logger")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s"))

logger.addHandler(stream_handler)


def wrap(pre, post):
    def decorator(function):
        def inner(*args, **kwargs):
            pre(function)
            result = function(*args, **kwargs)
            post(function)
            return result
        return inner
    return decorator


def entering(function):
    """ Entering function """
    logger.debug("Entered %s", function.__name__)


def exiting(function):
    """ Leaving function """
    logger.debug("Exited  %s", function.__name__)