import os
import pytest
import warnings
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import tapis


@pytest.mark.parametrize(
    "file_path, system_id, ftype, fname, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', 'file',
      'dawnofman.jpg', True)])
def test_tapis_stat_stat(agave, file_path, system_id, ftype, fname, test_pass):
    """Tapis stat returns the dict listing for a resource
    """

    def exceptable_test_code():
        resp = tapis.stat(file_path, system_id=system_id, agave=agave)
        assert resp.type == ftype
        assert resp.name == fname

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(Exception):
            exceptable_test_code()


@pytest.mark.parametrize(
    "file_path, system_id, test_exists",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True),
     ('/sample/tacc-cloud', 'data-sd2e-community', True),
     ('/sample/tacc-cloud/', 'data-sd2e-community', True),
     ('/sample/tacc-meep', 'data-sd2e-community', False)])
def test_tapis_stat_exists(agave, file_path, system_id, test_exists):
    """Determine existence of a resource via Tapis files
    """
    assert tapis.exists(
        file_path, system_id=system_id, agave=agave) == test_exists


@pytest.mark.parametrize(
    "file_path, system_id, test_isfile, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', True, True),
     ('/sample/tacc-cloud', 'data-sd2e-community', False, True),
     ('/sample/tacc-cloud/', 'data-sd2e-community', False, True),
     ('/sample/tacc-meep', 'data-sd2e-community', False, False),
     ('/sample/tacc-cloud/dawnofman.jpg', 'data-projects-safegenes', False,
      False), ('/uploads', 'data-projects-safegenes', False, True)])
def test_tapis_stat_isfile(agave, file_path, system_id, test_isfile,
                           test_pass):
    """Determine resource is a file via Tapis files
    """

    def exceptable_test_code():
        assert tapis.isfile(
            file_path, system_id=system_id, agave=agave) == test_isfile

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(tapis.exceptions.HTTPError):
            exceptable_test_code()


@pytest.mark.parametrize(
    "file_path, system_id, test_isfile, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', False, True),
     ('/sample/tacc-cloud', 'data-sd2e-community', True, True),
     ('/sample/tacc-cloud/', 'data-sd2e-community', True, True),
     ('/sample/tacc-meep', 'data-sd2e-community', False, False),
     ('/sample/tacc-cloud/dawnofman.jpg', 'data-projects-safegenes', False,
      False), ('/uploads', 'data-projects-safegenes', True, True)])
def test_tapis_stat_isdir(agave, file_path, system_id, test_isfile, test_pass):
    """Determine resource is a directory via Tapis files
    """

    def exceptable_test_code():
        assert tapis.isdir(
            file_path, system_id=system_id, agave=agave) == test_isfile

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(tapis.exceptions.HTTPError):
            exceptable_test_code()
