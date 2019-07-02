import os
import pytest
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')

from bacanora import direct


def test_direct_abs_path_localhost(agave):
    cwd = os.getcwd()
    ap = direct.abs_path('/sample/tacc-cloud/123', agave=agave)
    assert ap.startswith(cwd) is True


@pytest.mark.parametrize(
    "env_var, system_id, file_path, result",
    [('REACTORS_VERSION', 'data-sd2e-community', '/sample/tacc-cloud/123',
      '/work/projects/SD2E-Community/prod/data/sample/tacc-cloud/123'),
     ('JUPYTERHUB_USER', 'data-sd2e-community', '/sample/tacc-cloud/123',
      '/user/{User}/tree/sd2e-community/sample/tacc-cloud/123'),
     ('TACC_DOMAIN', 'data-sd2e-community', '/sample/tacc-cloud/123',
      '/work/projects/SD2E-Community/prod/data/sample/tacc-cloud/123'),
     ('REACTORS_VERSION', 'data-projects-safegenes', '/uploads/tacc',
      '/work/projects/DARPA-SD2-Partners/safegenes/uploads/tacc'),
     ('JUPYTERHUB_USER', 'data-projects-safegenes', '/uploads/tacc',
      '/user/{User}/tree/sd2e-partners/safegenes/uploads/tacc'),
     ('TACC_DOMAIN', 'data-projects-safegenes', '/uploads/tacc',
      '/work/projects/DARPA-SD2-Partners/safegenes/uploads/tacc'),
     ('REACTORS_VERSION', 'data-tacc-work-sd2eadm', '/share',
      '/work/05201/sd2eadm/share'),
     ('JUPYTERHUB_USER', 'data-tacc-work-sd2eadm', '/share',
      '/user/sd2eadm/tree/tacc-work/share'),
     ('TACC_DOMAIN', 'data-tacc-work-sd2eadm', '/share',
      '/work/05201/sd2eadm/share')])
def test_direct_abs_path_runtimes(monkeypatch, agave, env_var, system_id,
                                  file_path, result):
    """Host path can be resolved on the matrix of StorageSystem types
    and Bacanora runtimes
    """
    monkeypatch.setenv(env_var, 'NonEmptyIsAllWeNeed')
    ap = direct.abs_path(file_path, system_id=system_id, agave=agave)
    assert ap == result
