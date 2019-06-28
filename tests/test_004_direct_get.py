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


@pytest.mark.parametrize(
    "file_path, system_id, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', True)])
def test_direct_get_local_cwd(agave, file_path, system_id, test_pass):
    if test_pass:
        local_fname = os.path.basename(file_path)
        direct.get(file_path, system_id=system_id, agave=agave)
        files = os.listdir('.')
        assert local_fname in files
        os.unlink(local_fname)
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.get(file_path, system_id=system_id, agave=agave)


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'tmp/ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'dawnofman.jpg', True)])
def test_direct_get_local_named(agave, file_path, system_id, local_filename,
                                test_pass):

    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'
    if test_pass:
        direct.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.get(file_path, system_id=system_id, agave=agave)
    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'tmp/ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'dawnofman.jpg', True)])
def test_direct_get_local_no_atomic(agave, monkeypatch, file_path, system_id,
                                    local_filename, test_pass):
    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'
    if test_pass:
        direct.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            atomic=False,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files
    else:
        with pytest.raises(direct.DirectOperationFailed):
            direct.get(file_path, system_id=system_id, agave=agave)
    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))
