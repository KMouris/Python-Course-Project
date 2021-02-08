from config import logging


log_file = "./logfile.log"
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger("logger")


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
