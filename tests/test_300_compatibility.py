import os
import pytest
import warnings
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import compat, direct, runtimes, settings, tapis, utils
from .utils import local_delete


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'tmp/ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'dawnofman.jpg', True)])
def test_compat_download(project_dir, localhost_runtime, agave, file_path,
                         system_id, local_filename, test_pass):
    """Backwards-compatible bacanora.download operation functions as intended
    """
    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'

    def exceptable_code():
        compat.download(
            agave,
            file_path,
            local_filename=local_filename,
            system_id=system_id)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png',
      '/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_compat_upload(project_dir, localhost_runtime, agave, file_path,
                       destination_dir, system_id, test_pass):
    """Backwards-compatible bacanora.upload operation functions as intended
    """
    local_dest_dir = utils.normalize(destination_dir)

    def exceptable_code():
        compat.upload(agave, file_path, destination_dir, system_id=system_id)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(file_path) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        os.unlink(os.path.join(local_dest_dir, os.path.basename(file_path)))
    except SystemError:
        raise
        warnings.warn('Failed to unlink {}'.format(file_path))


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # directory exists
        ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
         True),
        # file exists
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-community', True, True),
        # fail because file cannot be found, raise UnknowableOutcome
        ('/tests/data/direct/sample/tacc-cloud/dawnofmeep.jpg',
         'data-sd2e-community', False, True),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-fake-system', False, True)
    ])
def test_compat_exists(project_dir, localhost_runtime, agave, file_path,
                       system_id, exists, test_pass):
    """Backwards-compatible bacanora.exists operation functions as intended
    """

    def exceptable_code():
        try:
            fp_exists = compat.exists(agave, file_path, system_id=system_id)
            if exists:
                assert fp_exists is exists, 'mismatched exists() result'
        except Exception:
            raise

    if test_pass:
        exceptable_code()
    else:
        if exists:
            with pytest.raises(direct.UnknowableOutcome):
                exceptable_code()
        else:
            with pytest.raises(direct.DirectOperationFailed):
                exceptable_code()


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # path exists but is directory
        ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', False,
         True),
        # path exists and is directory
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-community', True, True),
        # fail because file not found, raise UnknowableOutcome
        ('/tests/data/direct/sample/tacc-cloud/dawnofmeep.jpg',
         'data-sd2e-community', False, True),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-fake-system', False, True)
    ])
def test_compat_isfile(project_dir, localhost_runtime, agave, file_path,
                       system_id, exists, test_pass):
    """Backwards-compatible bacanora.isfile operation functions as intended
    """

    def exceptable_code():
        try:
            fp_exists = compat.exists(agave, file_path, system_id=system_id)
            if exists:
                assert fp_exists is exists, 'mismatched exists() result'
        except Exception:
            raise

    if test_pass:
        exceptable_code()
    else:
        if exists:
            with pytest.raises(direct.UnknowableOutcome):
                exceptable_code()
        else:
            with pytest.raises(direct.DirectOperationFailed):
                exceptable_code()


@pytest.mark.parametrize(
    "path_to_make, system_id, root_dir, force_action, test_pass, last_test",
    [('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      True, True, False),
     ('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      False, False, False),
     ('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      True, True, True),
     ('test-mkdir-relative', 'data-sd2e-community',
      '/tests/data/direct/sample', True, True, True)])
def test_compat_mkdir(project_dir, localhost_runtime, agave, path_to_make,
                      system_id, root_dir, force_action, test_pass, last_test):
    """Backwards-compatible bacanora.mkdir operation functions as intended
    """
    final_path_to_make = os.path.join(root_dir, utils.normalize(path_to_make))

    def exceptable_code():
        created_posix_path = direct.abs_path(
            path_to_make,
            system_id=system_id,
            root_dir=root_dir,
            runtime=runtimes.LOCALHOST,
            agave=agave)
        compat.mkdir(agave, path_to_make, system_id=system_id)
        if force_action:
            assert os.path.exists(
                created_posix_path), '{} did not exist after mkdir()'.format(
                    created_posix_path)
        # direct.exists(
        #     path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    if last_test:
        local_delete(final_path_to_make)
