import os
import pytest
import warnings
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

import bacanora


@pytest.mark.parametrize(
    "file_path, system_id, test_exists",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True),
     ('/sample/tacc-cloud', 'data-sd2e-community', True),
     ('/sample/tacc-cloud/', 'data-sd2e-community', True),
     ('/sample/tacc-meep', 'data-sd2e-community', False),
     ('/sample/tacc-cloud', 'data-projects-noop', False)])
def test_bacanora_exists(agave, file_path, system_id, test_exists):
    """Determine existence of a resource via Tapis files
    """
    assert bacanora.files.exists(
        file_path, system_id=system_id, agave=agave) == test_exists


@pytest.mark.parametrize(
    "file_path, system_id, test_isfile, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True, True),
     ('/sample/tacc-cloud', 'data-sd2e-community', False, True),
     ('/sample/tacc-cloud/', 'data-sd2e-community', False, True),
     ('/sample/tacc-meep', 'data-sd2e-community', False, False),
     ('/sample/tacc-cloud/dawnofman.jpg', 'data-projects-safegenes', False,
      False), ('/uploads', 'data-projects-safegenes', False, True)])
def test_bacanora_isfile(agave, file_path, system_id, test_isfile, test_pass):
    """Determine resource is a file via Tapis files
    """

    def exceptable_code():
        assert bacanora.files.isfile(
            file_path, system_id=system_id, agave=agave) == test_isfile

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(bacanora.ProcessingOperationFailed):
            exceptable_code()
