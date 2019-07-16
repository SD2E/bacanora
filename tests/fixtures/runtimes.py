import os
import pytest

__all__ = [
    'localhost_runtime', 'abaco_runtime', 'hpc_runtime', 'jupyter_runtime'
]


@pytest.fixture(scope='function')
def localhost_runtime(monkeypatch):
    monkeypatch.setenv('LOCALONLY', '1')


@pytest.fixture(scope='function')
def abaco_runtime(monkeypatch):
    monkeypatch.setenv('REACTORS_VERSION', '1')


@pytest.fixture(scope='function')
def hpc_runtime(monkeypatch):
    monkeypatch.setenv('TACC_DOMAIN', '1')


@pytest.fixture(scope='function')
def jupyter_runtime(monkeypatch):
    monkeypatch.setenv('JUPYTERHUB_USER', '1')
