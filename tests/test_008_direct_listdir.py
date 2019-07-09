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
    "abs_file_path, system_id, runtime, tapis_file_path,test_pass",
    [('/work/projects/SD2E-Community/prod/data/sample/tacc-cloud',
      'data-sd2e-community', 'hpc', '/sample/tacc-cloud', True),
     ('/user/{User}/tree/sd2e-community/sample/tacc-cloud',
      'data-sd2e-community', 'jupyter', '/sample/tacc-cloud', True),
     ('/work/05201/sd2eadm/share', 'data-tacc-work-sd2eadm', 'hpc', '/share',
      True),
     ('/user/sd2eadm/tree/tacc-work/share', 'data-tacc-work-sd2eadm',
      'jupyter', '/share', True),
     (os.path.join(CWD, 'tests/data/direct/sample'), 'data-sd2e-community',
      'localhost', '/tests/data/direct/sample', True)])
def test_abs_path_to_tapis(agave, abs_file_path, runtime, system_id,
                           tapis_file_path, test_pass):
    """Exercise reversal of utils.abs_path, which is used in direct.listdir()
    """

    def exceptable_test_code():
        path = direct.abspath_to_tapis(
            abs_file_path,
            system_id=system_id,
            root_dir='/',
            runtime=runtime,
            agave=agave)
        assert path == tapis_file_path

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_test_code()
