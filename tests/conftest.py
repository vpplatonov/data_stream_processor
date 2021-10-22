import glob
import os.path
import shutil

import pytest

from app.main import init


@pytest.fixture(name="csv_gen", scope="module")
def get_csv_cases():
    files = glob.glob('../tests/csv/*.csv')

    for name in files:
        shutil.copy(name, os.path.abspath('../csv/'))

    yield glob.glob('../csv/*.csv')

    for name in files:
        name = os.path.sep.join(name.split(os.path.sep)[2:])
        os.remove(os.path.join('../', name))


@pytest.fixture(name="app", scope="module")
def get_app():
    app = init()
    yield app


def test_read_csv(csv_gen):
    csv_files = glob.glob('../csv/*.csv')

    assert csv_files

