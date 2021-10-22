import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class Alerter:
    # Define static method, so no self parameter

    @staticmethod
    def process(df, num_error: int = 10):
        # Some prints to identify which plugin is been used
        # Alert over 10 error or fatal logs in less than an hour for a specific bundle id
        try:
            # df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H")
            df['hours'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H')).astype(int)
            alerter = df.groupby(["bundle_id", "hours"])["datetime"].count().to_numpy()
            res = alerter[alerter > num_error]
            if res:
                logger.error(f"{res}")

            return res
        except Exception as e:
            logger.exception(e)
