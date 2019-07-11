import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import direct, runtimes, utils


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png',
      '/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_direct_put_local(project_dir, agave, file_path, destination_dir,
                          system_id, test_pass):
    """Direct mode upload works in localhost runtime
    """
    local_dest_dir = utils.normalize(destination_dir)
    if test_pass:
        direct.put(
            file_path,
            destination_dir,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(file_path) in files
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.put(
                file_path,
                destination_dir,
                system_id=system_id,
                runtime=runtimes.LOCALHOST,
                agave=agave)
    try:
        os.unlink(os.path.join(local_dest_dir, os.path.basename(file_path)))
    except SystemError:
        raise
        warnings.warn('Failed to unlink {}'.format(file_path))


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png',
      '/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_direct_put_local_no_atomic(project_dir, agave, file_path,
                                    destination_dir, system_id, test_pass):
    """Direct mode upload works in localhost runtime without
    atomic operation support
    """
    local_dest_dir = utils.normalize(destination_dir)
    if test_pass:
        direct.put(
            file_path,
            destination_dir,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            agave=agave)
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.put(
                file_path,
                destination_dir,
                system_id=system_id,
                runtime=runtimes.LOCALHOST,
                atomic=False,
                agave=agave)
    try:
        os.unlink(os.path.join(local_dest_dir, os.path.basename(file_path)))
    except SystemError:
        raise
        warnings.warn('Failed to unlink {}'.format(file_path))
