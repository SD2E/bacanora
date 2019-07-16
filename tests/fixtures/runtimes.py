import os
import pytest

__all__ = [
    'localhost_runtime', 'abaco_runtime', 'jupyter_runtime',
    'hpc_jupyter_runtime', 'hpc_runtime'
]


@pytest.fixture(scope='function')
def localhost_runtime(monkeypatch):
    monkeypatch.setenv('LOCALONLY', '1')


@pytest.fixture(scope='function')
def abaco_runtime(monkeypatch):
    monkeypatch.setenv('REACTORS_VERSION', '0.7.0')
    monkeypatch.setenv('_abaco_actor_dbid', 'SD2E_0mvZjDe6l8e8L')


@pytest.fixture(scope='function')
def jupyter_runtime(monkeypatch):
    monkeypatch.setenv('JUPYTERHUB_USER', 'taco')
    monkeypatch.setenv('JUPYTERHUB_API_TOKEN',
                       '18851749b0b641a8a5dd842fcfb83dac')


@pytest.fixture(scope='function')
def hpc_jupyter_runtime(monkeypatch):
    monkeypatch.setenv('TACC_DOMAIN', 'wrangler')
    monkeypatch.setenv('TACC_SINGULARITY_DIR',
                       '/opt/apps/tacc-singularity/2.6.0')
    monkeypatch.setenv('JUPYTER_WORK', '/work/03762/eriksf/jupyter_packages')


@pytest.fixture(scope='function')
def hpc_runtime(monkeypatch):
    monkeypatch.setenv('TACC_DOMAIN', 'wrangler')
    monkeypatch.setenv('TACC_SYSTEM', 'Wrangler')
    monkeypatch.setenv('SLURM_CLUSTER_NAME', 'Wrangler')
