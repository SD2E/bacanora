import os
import pytest

CWD = os.getcwd()
TMP_DIR = os.path.join(CWD, 'tmp')
DATA_DIR = os.path.join(CWD, 'tests', 'data', 'direct')

__all__ = ['project_dir', 'project_dir_tmp', 'project_tests_data_dir']


@pytest.fixture(scope='function')
def project_dir(monkeypatch):
    monkeypatch.setenv('BACANORA_LOCALHOST_ROOT_DIR', CWD)


@pytest.fixture(scope='function')
def project_dir_tmp(monkeypatch):
    monkeypatch.setenv('BACANORA_LOCALHOST_ROOT_DIR', TMP_DIR)


@pytest.fixture(scope='function')
def project_tests_data_dir(monkeypatch):
    monkeypatch.setenv('BACANORA_LOCALHOST_ROOT_DIR', DATA_DIR)
