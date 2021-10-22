import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Alerter:
    # Define static method, so no self parameter

    @staticmethod
    def process(data):
        # Some prints to identify which plugin is been used
        logger.info(f"{__name__} alert")
        try:
            logger.info(data)
        except Exception as e:
            logger.exception(e)
