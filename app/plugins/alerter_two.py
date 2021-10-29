import pandas as pd


class AlerterTwo:
    # Define static method, so no self parameter

    @staticmethod
    def process(df, num_error: int = 10, bundle_id=None, logger=None, **kwargs):
        # Some prints to identify which plugin is been used
        # Alert over 10 error or fatal logs in less than an hour for a specific bundle id
        if logger is None:
            raise Exception("logger is not available")

        if bundle_id is None:
            raise Exception("bundle_id is not available")

        try:
            # df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H")
            df['hours'] = df['datetime'].apply(lambda x: x.strftime('%Y%m%d%H')).astype(int)
            alerter = df[df["bundle_id"] == bundle_id].groupby(["hours"])["datetime"].count().to_numpy()
            res = alerter[alerter > num_error]
            if res:
                logger.info(f"{__name__}: {res}")

            return res
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def test_case():
        """ test case for CI/CD """

        columns = ["error_type", "datetime", "bundle_id"]
        data = [["fatal", "20211021 22:22:22", "alerter_one"],
                ["fatal", "20211021 22:22:23", "alerter_two"],
                ["error", "20211021 22:22:24", "alerter_two"],
                ["fatal", "20211021 22:22:25", "alerter_two"],
                ["error", "20211021 23:26:24", "alerter_two"],
                ["error", "20211021 23:27:25", "alerter_one"]]
        df = pd.DataFrame(data, columns=columns)
        df['datetime'] = pd.to_datetime(df['datetime'])

        kw = dict(
            df=df,
            num_error=1,
            bundle_id="alerter_two",
            assertion=[3]
        )

        return kw
