import pandas as pd
import pytest

from app.main import chunksize, chunk_generator


@pytest.fixture(name="chunk", scope="function")
def get_chunk(csv_gen, app):

    for chunk, file, idx in chunk_generator(csv_gen):
        yield chunk, file, idx


@pytest.fixture(name="plugin_one", scope="function")
def get_plugin_one(app):
    yield app._plugins[0]


@pytest.fixture(name="plugin_two", scope="function")
def get_plugin_two(app):
    yield app._plugins[1]


def test_main(csv_gen, app):

    assert csv_gen

    for file in csv_gen:
        with pd.read_csv(file, chunksize=chunksize, parse_dates=["datetime"]) as reader:
            for chunk in reader:
                assert not chunk.empty


def test_plugin_one(chunk, plugin_one):
    chnk, file, idx = chunk
    assert not chnk.empty
    assert idx == 0
    # assert num_iter == 1
    assert isinstance(file, str)

    try:
        plugin_one.process(chnk, num_error=1)
    except Exception as e_info:
        pytest.fail(f"{e_info}")


def test_plugin_two(chunk, plugin_two):
    chnk, file, idx = chunk
    assert not chnk.empty

    try:
        plugin_two.process(chnk, num_error=1)
    except Exception as e_info:
        pytest.fail(f"{e_info}")
