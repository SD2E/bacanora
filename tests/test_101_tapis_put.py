import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import tapis
from bacanora.exceptions import AgaveError, HTTPError, HTTPNotFoundError
from bacanora.tapis import TapisOperationFailed


@pytest.mark.parametrize(
    "file_path, destination_dir, system_id, test_pass",
    [('tests/data/direct/put/foodtruck.png', '/sample/tacc-cloud',
      'data-sd2e-community', True),
     ('tests/data/direct/put/foodtruck.png',
      '/sample/tacc-cloud/compat-upload', 'data-sd2e-community', False)])
def test_tapis_put(project_tests_data_dir, abaco_runtime, agave, file_path,
                   destination_dir, system_id, test_pass):
    """Tapis files-upload works as intended
    """

    def exceptable_code():
        tapis.put(
            file_path,
            destination_dir,
            system_id=system_id,
            force=True,
            agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()

    try:
        tapis.delete(
            os.path.join(destination_dir, os.path.basename(file_path)),
            system_id=system_id,
            agave=agave)
    except Exception:
        warnings.warn('Failed to delete {}'.format(file_path))


@pytest.mark.parametrize("file_path, destination_dir, system_id, test_pass",
                         [('tests/data/direct/put/foodtruck.png',
                           '/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_tapis_put_atomic(project_tests_data_dir, abaco_runtime, agave,
                          file_path, destination_dir, system_id, test_pass):
    """Tapis files-upload works with atomic mode
    """

    def exceptable_code():
        tapis.put(
            file_path,
            destination_dir,
            system_id=system_id,
            force=True,
            atomic=True,
            agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()

    try:
        tapis.delete(
            os.path.join(destination_dir, os.path.basename(file_path)),
            system_id=system_id,
            agave=agave)
    except Exception:
        warnings.warn('Failed to delete {}'.format(file_path))


@pytest.mark.parametrize("file_path, destination_dir, system_id, test_pass",
                         [('tests/data/direct/put/foodtruck.png',
                           '/sample/tacc-cloud', 'data-sd2e-community', True)])
def test_tapis_put_sync(project_tests_data_dir, abaco_runtime, agave,
                        file_path, destination_dir, system_id, test_pass):
    """Tapis files-upload works with sync mode
    """

    def exceptable_code():
        tapis.put(
            file_path,
            destination_dir,
            system_id=system_id,
            sync=True,
            atomic=True,
            force=True,
            agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()

    # try:
    #     tapis.delete(
    #         os.path.join(destination_dir, os.path.basename(file_path)),
    #         system_id=system_id,
    #         agave=agave)
    # except Exception:
    #     warnings.warn('Failed to delete {}'.format(file_path))
