import functools
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def log_function(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info(f"{func_name} started")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func_name} ended")
            return result
        except Exception as e:
            logger.error(f"There was an error in {func_name}: {e}")
            raise
    return wrapper
