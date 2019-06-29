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


@pytest.mark.parametrize("path_to_make, system_id, test_pass",
                         [('/tests/data/direct/sample/test-mkdir-absolute',
                           'data-sd2e-community', True)])
def test_direct_manage_all_absolute(agave, path_to_make, system_id, test_pass):
    """Permutations of mkdir (rooted, relative, nested, etc) work as intended
    """

    def exceptable_test_code():
        path_made_new_name = path_to_make + '-renamed'
        direct.mkdir(path_to_make, system_id=system_id, agave=agave)
        direct.exists(path_to_make, system_id=system_id, agave=agave)
        direct.rename(
            path_to_make, path_made_new_name, system_id=system_id, agave=agave)
        direct.delete(path_made_new_name, system_id=system_id, agave=agave)

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_test_code()


@pytest.mark.parametrize("path_to_make, system_id, root_dir, test_pass",
                         [('test-mkdir-relative', 'data-sd2e-community',
                           '/tests/data/direct/sample', True)])
def test_direct_manage_all_relative(agave, path_to_make, system_id, root_dir,
                                    test_pass):
    """Permutations of mkdir (rooted, relative, nested, etc) work as intended
    """

    def exceptable_test_code():
        direct.mkdir(
            path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)
        direct.exists(
            path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)
        direct.delete(
            path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_test_code()
