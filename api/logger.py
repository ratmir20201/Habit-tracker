import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger(__name__)
