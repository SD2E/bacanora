import os
import pytest

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/stores')

from bacanora import stores, runtimes


@pytest.mark.parametrize("string_value, test_pass",
                         [('data-sd2e-community', True), ('deadbeef', False),
                          (None, False)])
def test_stores_storage_system(agave, string_value, test_pass):
    """Can init the StorageSystem mapping client with valid system_id
    """
    if test_pass:
        assert stores.StorageSystem(string_value, agave=agave) is not None
    else:
        with pytest.raises(ValueError):
            stores.StorageSystem(string_value, agave=agave)


@pytest.mark.parametrize("system_id, sys_type, sys_short_name", [
    ('data-sd2e-community', stores.COMMUNITY_TYPE, 'sd2e-community'),
    ('data-tacc-work-sd2eadm', stores.WORK_TYPE, 'sd2eadm'),
    ('data-projects-echo', stores.PROJECT_TYPE, 'echo'),
    ('data-sd2e-projects.sd2e-project-4', stores.SHARE_TYPE, 'sd2e-project-4')
])
def test_stores_type_shortname(agave, system_id, sys_type, sys_short_name):
    """Determine system type and short name based from system_id
    """
    ss = stores.StorageSystem(system_id, agave=agave)
    assert ss._type == sys_type
    assert ss._short_name == sys_short_name


@pytest.mark.parametrize(
    "runtime, system_id, file_path, result",
    [(runtimes.ABACO, 'data-sd2e-community', '/uploads',
      '/work/projects/SD2E-Community/prod/data/uploads'),
     (runtimes.JUPYTER, 'data-sd2e-community', '/uploads',
      '/user/{User}/tree/sd2e-community/uploads'),
     (runtimes.HPC, 'data-sd2e-community', '/uploads',
      '/work/projects/SD2E-Community/prod/data/uploads'),
     (runtimes.ABACO, 'data-tacc-work-sd2eadm', '/share',
      '/work/05201/sd2eadm/share'),
     (runtimes.ABACO, 'data-tacc-work-vaughn', '/share',
      '/work/01374/vaughn/share'),
     (runtimes.HPC, 'data-tacc-work-sd2eadm', '/share',
      '/work/05201/sd2eadm/share'),
     (runtimes.HPC, 'data-tacc-work-vaughn', '/share',
      '/work/01374/vaughn/share'),
     (runtimes.JUPYTER, 'data-tacc-work-sd2eadm', '/share',
      '/user/sd2eadm/tree/tacc-work/share'),
     (runtimes.ABACO, 'data-projects-echo', '/uploads',
      '/work/projects/DARPA-SD2-Partners/echo/uploads'),
     (runtimes.ABACO, 'data-projects-safegenes', '/uploads',
      '/work/projects/DARPA-SD2-Partners/safegenes/uploads'),
     (runtimes.HPC, 'data-projects-safegenes', '/uploads',
      '/work/projects/DARPA-SD2-Partners/safegenes/uploads'),
     (runtimes.JUPYTER, 'data-projects-safegenes', '/uploads',
      '/user/{User}/tree/sd2e-partners/safegenes/uploads'),
     (runtimes.ABACO, 'data-sd2e-projects.sd2e-project-4', '/',
      '/work/projects/SD2E-Community/prod/projects/sd2e-project-4'),
     (runtimes.JUPYTER, 'data-sd2e-projects.sd2e-project-4', '/',
      '/user/{User}/tree/sd2e-projects/sd2e-project-4'),
     (runtimes.HPC, 'data-sd2e-projects.sd2e-project-4', '/',
      '/work/projects/SD2E-Community/prod/projects/sd2e-project-4'),
     (runtimes.HPC, 'data-sd2e-projects-users', '/sd2eadm',
      '/work/projects/SD2E-Community/prod/share/sd2eadm'),
     (runtimes.ABACO, 'data-sd2e-projects-users', '/sd2eadm',
      '/work/projects/SD2E-Community/prod/share/sd2eadm')])
def test_stores_runtime_dir(agave, runtime, system_id, file_path, result):
    """Validate the main function of StorageSystem: Given a runtime name
    and path, resolve the full, absolute path on the runtime host
    """
    ss = stores.StorageSystem(system_id, agave=agave)
    ss_path = ss.runtime_dir(runtime, file_path)
    assert ss_path.startswith(result)


@pytest.mark.parametrize(
    "system_id, file_path, result",
    [('data-sd2e-community', '/sample', 'agave://data-sd2e-community/sample'),
     ('data-tacc-work-sd2eadm', '/share',
      'agave://data-tacc-work-sd2eadm/share')])
def test_agave_canoncial_uri(agave, system_id, file_path, result):
    uri = stores.StorageSystem(
        system_id, agave=agave).agave_canonical_uri(file_path)
    assert uri == result


@pytest.mark.parametrize("system_id, file_path, result", [
    ('data-sd2e-community', '/sample',
     'https://api.sd2e.org/files/v2/media/system/data-sd2e-community/sample'),
    ('data-tacc-work-sd2eadm', '/share',
     'https://api.sd2e.org/files/v2/media/system/data-tacc-work-sd2eadm/share')
])
def test_agave_http_uri(agave, system_id, file_path, result):
    uri = stores.StorageSystem(
        system_id, agave=agave).agave_http_uri(file_path)
    assert uri == result


@pytest.mark.parametrize(
    "system_id, file_path, result",
    [('data-sd2e-community', '/sample',
      'https://jupyter.sd2e.org/user/{User}/tree/sd2e-community/sample'),
     ('data-tacc-work-sd2eadm', '/share',
      'https://jupyter.sd2e.org/user/sd2eadm/tree/tacc-work/share')])
def test_jupyterhub_http_uri(agave, system_id, file_path, result):
    uri = stores.StorageSystem(
        system_id, agave=agave).jupyterhub_http_uri(file_path)
    assert uri == result


@pytest.mark.parametrize("system_id, file_path, result", [
    ('data-sd2e-community', '/sample',
     'sftp://tacobot@data.sd2e.org:22/work/projects/SD2E-Community/prod/data/sample'
     ),
    ('data-tacc-work-sd2eadm', '/share',
     'sftp://tacobot@users-data.sd2e.org:2222/work/05201/sd2eadm/share'),
    ('data-projects-safegenes', '/uploads',
     'sftp://tacobot@cloud.corral.tacc.utexas.edu:2222/work/projects/DARPA-SD2-Partners/safegenes/uploads'
     )
])
def test_jupyterhub_http_uri(agave, system_id, file_path, result):
    uri = stores.StorageSystem(
        system_id, agave=agave).sftp_uri(
            file_path, username='tacobot')
    assert uri == result
