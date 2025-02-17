import logging

logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter(
    fmt="%(levelname)s | %(name)s | %(asctime)s |  %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger(__name__)

custom_handler = logging.StreamHandler()
logger.addHandler(custom_handler)
custom_handler.setFormatter(formatter)
