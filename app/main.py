import glob
import logging
import os
from time import sleep

import pandas as pd

from core import DataStreamProcessor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

file_prefix = '../'
plugins_path = 'plugins'
chunksize = 1000
num_error = 1


def init():
    # get list of Alerter plugins
    plugins = ["." + file.split(".py")[0].split(f"{plugins_path}/")[1]
               for file in glob.glob(plugins_path + '/alerter*.py')]
    # Initialising our application
    app = DataStreamProcessor(
        plugins=plugins,
        path=plugins_path
    )

    return app


def file_list_prepare(del_processed=True):
    while True:
        # Running our application
        csv_files = glob.glob(os.path.join(file_prefix, 'csv/*.csv'))

        if not csv_files:
            logger.info("no files for processing")
            sleep(1)
            continue

        for file in csv_files:

            yield file

        # remove file after processing
        if del_processed:
            for file in csv_files:
                os.remove(file)


def chunk_generator(csv_files: iter):
    """
    Generate chuck of pandas dataframe continuously.
    Sleep if stream is empty.

    :return: yield chunk, file, idx
    """

    for file in csv_files:
        logger.info(f"{file=} processing")

        with pd.read_csv(
                file,
                chunksize=chunksize,
                parse_dates=["datetime"]
        ) as reader:

            # num_iter = reader.len()
            for idx, chunk in enumerate(reader):
                yield chunk, file, idx  # , num_iter


def main(del_processed=True):

    app = init()

    for chunk, file, idx in chunk_generator(
            file_list_prepare(del_processed=del_processed)
    ):
        app.run(df=chunk, num_error=num_error, logger=logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logger.info(f"interrupted with {e.__cause__}")
