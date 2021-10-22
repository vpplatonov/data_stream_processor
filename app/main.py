import glob
import logging
import os
from time import sleep

import pandas as pd

from core import DataStreamProcessor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

plugins_path = 'plugins'
chunksize = 1000
num_error = 1


def init():
    # get list of Alerter plugins
    plugins = ["." + file.split(".py")[0].split("plugins/")[1]
               for file in glob.glob(plugins_path + '/alerter*.py')]
    # Initialising our application
    app = DataStreamProcessor(
        plugins=plugins,
        path=plugins_path
    )

    return app


def file_list_prepare():
    while True:
        # Running our application
        csv_files = glob.glob('../csv/*.csv')

        if not csv_files:
            logger.info("no files for processing")
            sleep(1)
            continue

        # remove file after processing
        for file in csv_files:
            logger.info(f"{file=} processing")

            yield file

            os.remove(file)


def chunk_generator(csv_files: iter):
    """
    Generate chuck of pandas dataframe continuously.
    Sleep if stream is empty.

    :return: yield chunk, file, idx
    """

    for file in csv_files:
        with pd.read_csv(file, chunksize=chunksize, parse_dates=["datetime"]) as reader:

            # num_iter = reader.len()
            for idx, chunk in enumerate(reader):
                yield chunk, file, idx  # , num_iter


def main():

    app = init()

    file_list = list(file_list_prepare())
    for chunk, file, idx in chunk_generator(file_list):
        app.run(df=chunk, num_error=num_error)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logger.info(f"interrupted with {e.__cause__}")
