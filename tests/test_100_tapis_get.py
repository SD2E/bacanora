import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import tapis
from bacanora.exceptions import HTTPError, HTTPNotFoundError


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', None, True)])
def test_tapis_get(agave, file_path, system_id, local_filename, test_pass):
    def exceptable_code():
        downloaded_filename = tapis.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            atomic=True,
            agave=agave)
        os.unlink(downloaded_filename)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/sample/tacc-cloud/dawnofdog.jpg', 'data-sd2e-community', None, False),
     ('/sample/tacc-cloud/dawnofman.jpg', 'data-projects-safegenes', None,
      False)])
def test_tapis_get_httperror(agave, file_path, system_id, local_filename,
                             test_pass):
    def exceptable_code():
        downloaded_filename = tapis.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            atomic=True,
            agave=agave)
        os.unlink(downloaded_filename)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(HTTPNotFoundError):
            exceptable_code()
