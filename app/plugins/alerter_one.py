import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Alerter:
    # Define static method, so no self parameter

    @staticmethod
    def process(df, num_error: int = 10):
        # Some prints to identify which plugin is been used
        # Alert over 10 fatal logs in less than a minute (you have DateTime)
        try:
            # df['datetime'] = pd.to_datetime(df['datetime'], format="%Y %m %d %H:%M")
            df['minutes'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H%M')).astype(int)
            alerter = df[df.error_type == "fatal"].groupby(["minutes"])["datetime"].count().to_numpy()
            if alerter[alerter > num_error]:
                logger.error(f"{alerter[alerter > num_error]}")
        except Exception as e:
            logger.exception(e)
