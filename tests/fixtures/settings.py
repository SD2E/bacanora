import os
import pytest

CWD = os.getcwd()
TMP_DIR = os.path.join(CWD, 'tmp')

__all__ = ['project_dir', 'project_dir_tmp']


@pytest.fixture(scope='function')
def project_dir(monkeypatch):
    monkeypatch.setenv('BACANORA_LOCALHOST_ROOT_DIR', CWD)


@pytest.fixture(scope='function')
def project_dir_tmp(monkeypatch):
    monkeypatch.setenv('BACANORA_LOCALHOST_ROOT_DIR', TMP_DIR)
