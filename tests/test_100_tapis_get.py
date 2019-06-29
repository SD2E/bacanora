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
    "file_path, system_id, local_filename, test_pass",
    [('/sample/tacc-cloud/dawnofman.jpg', 'data-sd2e-community', None, True)])
def test_tapis_get(agave, file_path, system_id, local_filename, test_pass):
    def exceptable_test_code():
        downloaded_filename = tapis.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            atomic=True,
            agave=agave)
        os.unlink(downloaded_filename)

    if test_pass:
        exceptable_test_code()
    else:
        with pytest.raises(tapis.DirectOperationFailed):
            exceptable_test_code()
