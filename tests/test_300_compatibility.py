import os
import pytest
import warnings
from agavepy.agave import AgaveError
from bacanora.exceptions import HTTPNotFoundError

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import compat, direct, runtimes, settings, tapis, utils
from .utils import local_delete

# This array is populated wit tuples of system_id, file_path. Each will be
# deleted (or an attempt made) in test_compat_cleanup()
RESOURCES_TO_DELETE = list()


@pytest.mark.parametrize("file_path, system_id, local_filename, test_pass",
                         [('/sample/tacc-cloud/dawnofman.jpg',
                           'data-sd2e-community', 'ape.jpg', True),
                          ('/sample/tacc-cloud/dawnofman.jpg',
                           'data-sd2e-community', 'tmp/ape.jpg', True),
                          ('/sample/tacc-cloud/dawnofman.jpg',
                           'data-projects-safejeeps', 'dawnofman.jpg', False)])
def test_compat_download(project_tests_data_dir, localhost_runtime, agave,
                         file_path, system_id, local_filename, test_pass):
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
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()

    try:
        os.unlink(local_fname)
    except (FileNotFoundError, IOError, SystemError):
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png', '/sample/tacc-cloud',
      'data-sd2e-community', True),
     ('tests/data/direct/put/yakshave.png', '/sample/tacc-cloud/compat-upload',
      'data-sd2e-community', True)])
def test_compat_upload(project_tests_data_dir, localhost_runtime, agave,
                       file_path, destination_dir, system_id, test_pass):
    """Backwards-compatible bacanora.upload operation functions as intended
    """
    local_dest_dir = os.path.join(DATA_DIR, utils.normalize(destination_dir))

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
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/yakshave.png', '/sample/tacc-cloud',
      'data-sd2e-community', True),
     ('tests/data/direct/put/yakshave.png', '/sample/tacc-cloud/compat-upload',
      'data-sd2e-community', True)])
def test_compat_upload_nomount(project_tests_data_dir, abaco_runtime, agave,
                               file_path, destination_dir, system_id,
                               test_pass):
    """Backwards-compatible bacanora.upload operation functions without local mount
    """
    remote_dest_path = os.path.join(destination_dir,
                                    os.path.basename(file_path))

    def exceptable_code():
        compat.upload(agave, file_path, destination_dir, system_id=system_id)
        # Do not use compat.exists or any abstracted API to check this
        file_record = agave.files.list(
            filePath=remote_dest_path, systemId=system_id, limit=2)[0]
        assert file_record.get('name', '') == os.path.basename(file_path)

    if test_pass:
        exceptable_code()
        RESOURCES_TO_DELETE.append((system_id, remote_dest_path))
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        # Do not use compat.delete or any abstracted API to clean up
        agave.files.delete(remote_dest_path, systemId=system_id)
    except Exception:
        warnings.warn(
            'Failed to delete {} from Tapis system'.format(file_path))


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # directory exists
        ('/sample/tacc-cloud', 'data-sd2e-community', True, True),
        # file exists
        ('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True, True
         ),
        # fail because file cannot be found, raise UnknowableOutcome
        ('/sample/tacc-cloud/dawnofmeep.jpg', 'data-sd2e-community', False,
         True),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-fake-system', False,
         True)
    ])
def test_compat_exists(project_tests_data_dir, localhost_runtime, agave,
                       file_path, system_id, exists, test_pass):
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
        ('/sample/tacc-cloud', 'data-sd2e-community', False, True),
        # path exists and is directory
        ('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True, True
         ),
        # fail because file not found, raise UnknowableOutcome
        ('/sample/tacc-cloud/dawnofmeep.jpg', 'data-sd2e-community', False,
         True),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-fake-system', False,
         True)
    ])
def test_compat_isfile(project_tests_data_dir, localhost_runtime, agave,
                       file_path, system_id, exists, test_pass):
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
    [('/sample/tacc-cloud/test-mkdir-force', 'data-sd2e-community', '/', True,
      True, False),
     ('/sample/tacc-cloud/test-mkdir-force', 'data-sd2e-community', '/', False,
      False, False),
     ('/sample/tacc-cloud/test-mkdir-force', 'data-sd2e-community', '/', True,
      True, True),
     ('test-mkdir-relative', 'data-sd2e-community', '/sample/tacc-cloud', True,
      True, True)])
def test_compat_mkdir(project_tests_data_dir, localhost_runtime, agave,
                      path_to_make, system_id, root_dir, force_action,
                      test_pass, last_test):
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
        RESOURCES_TO_DELETE.append((system_id, path_to_make))
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    if last_test:
        local_delete(final_path_to_make)


def test_compat_cleanup(abaco_runtime, agave):
    for system, path in RESOURCES_TO_DELETE:
        try:
            agave.files.delete(filePath=path, systemId=system)
        except Exception:
            warnings.warn('Delete failed for agave://{}{}'.format(
                system, path))
