import os
import pytest
import warnings
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')

from bacanora import direct


@pytest.mark.parametrize(
    "file_path, system_id, exists, isfile, isdir, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', True, True, False, True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-fake-system', True, True, False, False),
     ('/tests/data/direct/sample/tacc-cloud/', 'data-sd2e-community', True,
      False, True, True),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
      False, True, True)])
def test_direct_get_local_cwd(agave, file_path, system_id, exists, isfile,
                              isdir, test_pass):
    """Stat operations (exists, isfile, isdir) function in direct mode
    """
    if test_pass:
        fp_exists = direct.exists(file_path, system_id=system_id, agave=agave)
        fp_isfile = direct.isfile(file_path, system_id=system_id, agave=agave)
        fp_isdir = direct.isdir(file_path, system_id=system_id, agave=agave)
        assert fp_exists is exists
        assert fp_isfile is isfile
        assert fp_isdir is isdir
    else:
        with pytest.raises(direct.DirectOperationFailed):
            fp_exists = direct.exists(
                file_path, system_id=system_id, agave=agave)
            fp_isfile = direct.isfile(
                file_path, system_id=system_id, agave=agave)
            fp_isdir = direct.isdir(
                file_path, system_id=system_id, agave=agave)
            assert fp_exists is exists
            assert fp_isfile is isfile
            assert fp_isdir is isdir
