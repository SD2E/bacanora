import os
import pytest
import warnings
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import direct
from bacanora import utils


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png',
      '/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_direct_put_local(agave, file_path, destination_dir, system_id,
                          test_pass):
    local_dest_dir = utils.normalize(destination_dir)
    if test_pass:
        direct.put(
            file_path, destination_dir, system_id=system_id, agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(file_path) in files
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.put(
                file_path, destination_dir, system_id=system_id, agave=agave)
    try:
        os.unlink(os.path.join(local_dest_dir, os.path.basename(file_path)))
    except SystemError:
        raise
        warnings.warn('Failed to unlink {}'.format(file_path))


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png',
      '/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_direct_put_local_no_atomic(agave, file_path, destination_dir,
                                    system_id, test_pass):
    local_dest_dir = utils.normalize(destination_dir)
    if test_pass:
        direct.put(
            file_path, destination_dir, system_id=system_id, agave=agave)
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.put(
                file_path,
                destination_dir,
                system_id=system_id,
                atomic=False,
                agave=agave)
    try:
        os.unlink(os.path.join(local_dest_dir, os.path.basename(file_path)))
    except SystemError:
        raise
        warnings.warn('Failed to unlink {}'.format(file_path))
