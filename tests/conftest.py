import glob
import os.path
import shutil

import pytest

from app.main import init


@pytest.fixture(name="file_prefix", scope="module")
def get_file_prefix():
    return "../"


@pytest.fixture(name="csv_gen", scope="module")
def get_csv_cases(file_prefix):
    files = glob.glob(os.path.join(file_prefix, 'tests/csv/*.csv'))

    for name in files:
        shutil.copy(name, os.path.abspath(os.path.join(file_prefix, 'csv/')))

    yield glob.glob(os.path.join(file_prefix, 'csv/*.csv'))

    for name in files:
        idx = file_prefix.count(os.path.sep) + 1
        name = os.path.sep.join(name.split(os.path.sep)[idx:])
        os.remove(os.path.join(file_prefix, name))


@pytest.fixture(name="app", scope="module")
def get_app():
    app = init()
    yield app
