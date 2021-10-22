import pandas as pd
import pytest

from app.main import chunksize


@pytest.fixture(name="chunk", scope="function")
def get_chunk(csv_gen, app):
    for file in csv_gen:

        with pd.read_csv(file, chunksize=chunksize, iterator=True) as reader:

            # max_iter = reader.len()

            for idx, chunk in enumerate(reader):
                yield chunk, file, idx  # , max_iter


def test_main(csv_gen, app):

    assert csv_gen

    for file in csv_gen:
        with pd.read_csv(file, chunksize=chunksize) as reader:
            for chunk in reader:

                assert not chunk.empty

                try:
                    app.run(data=chunk)
                except Exception as e_info:
                    pytest.fail(f"{e_info}")


def test_plugin_one(chunk):
    chnk, file, idx = chunk
    assert not chnk.empty
    assert idx == 0
    # assert num_iter == 1
    assert isinstance(file, str)


def test_plugin_two(chunk):
    chnk, file, idx = chunk
    assert not chnk.empty
