
class Alerter:
    # Define static method, so no self parameter

    @staticmethod
    def process(df, num_error: int = 10, **kwargs):
        # Some prints to identify which plugin is been used
        # Alert over 10 fatal logs in less than a minute (you have DateTime)
        if "logger" not in kwargs:
            raise Exception("logger is not available")

        logger = kwargs["logger"]

        try:
            # df['datetime'] = pd.to_datetime(df['datetime'], format="%Y %m %d %H:%M")
            df['minutes'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H%M')).astype(int)
            alerter = df[df.error_type == "fatal"].groupby(["minutes"])["datetime"].count().to_numpy()
            res = alerter[alerter > num_error]
            if res:
                logger.info(f"{__name__}: {res}")

            return res
        except Exception as e:
            logger.exception(e)
