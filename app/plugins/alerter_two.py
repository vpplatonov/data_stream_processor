
class Alerter:
    # Define static method, so no self parameter

    @staticmethod
    def process(df, num_error: int = 10, **kwargs):
        # Some prints to identify which plugin is been used
        # Alert over 10 error or fatal logs in less than an hour for a specific bundle id
        if "logger" not in kwargs:
            raise Exception("logger is not available")

        if "bundle_id" not in kwargs:
            raise Exception("bundle_id is not available")

        try:
            # df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H")
            df['hours'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H')).astype(int)
            alerter = df[df["bundle_id"] == kwargs["bundle_id"]].groupby(["hours"])["datetime"].count().to_numpy()
            res = alerter[alerter > num_error]
            if res:
                kwargs["logger"].info(f"{__name__}: {res}")

            return res
        except Exception as e:
            kwargs["logger"].exception(e)
