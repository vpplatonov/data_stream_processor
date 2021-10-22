import os

import pandas as pd
from core import DataStreamProcessor
import glob
from time import sleep
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

plugins_path = 'plugins'
# Two strategies:
#   a lof of small files
#   each file too big
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


def chunk_generator():
    """
    Generate chuck of pandas dataframe continuously.
    Sleep if stream is empty.

    :return: yield
    """
    while True:
        # Running our application
        csv_files = glob.glob('../csv/*.csv')

        if not csv_files:
            logger.info("no files for processing")
            sleep(1)
            continue

        for file in csv_files:
            with pd.read_csv(file, chunksize=chunksize) as reader:

                num_iter = reader.len()

                for idx, chunk in enumerate(reader):
                    yield chunk, file, idx, num_iter

            # remove file after proccesing
            os.remove(file)


def main():

    app = init()

    for chunk, file, idx, num_iter in chunk_generator():
        app.run(data=chunk)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logger.info(f"interrupted with {e.__cause__}")
