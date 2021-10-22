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

        yield csv_files

        # remove file after processing
        for file in csv_files:
            os.remove(file)


def chunk_generator(csv_files: iter):
    """
    Generate chuck of pandas dataframe continuously.
    Sleep if stream is empty.

    :return: yield chunk, file, idx
    """

    for file in next(csv_files):
        with pd.read_csv(file, chunksize=chunksize, parse_dates=["datetime"]) as reader:

            # num_iter = reader.len()

            for idx, chunk in enumerate(reader):
                yield chunk, file, idx  # , num_iter


def main():

    app = init()

    for chunk, file, idx in chunk_generator(file_list_prepare()):
        app.run(data=chunk)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logger.info(f"interrupted with {e.__cause__}")
