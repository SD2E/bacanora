import os
import pytest
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')

from bacanora import direct


def test_direct_abs_path_localhost(agave):
    cwd = os.getcwd()
    ap = direct.abs_path('/sample/tacc-cloud/123', agave=agave)
    assert ap.startswith(cwd) is True


# @pytest.mark.parametrize("runtime, system_id, path, result",
#                          [('REACTORS_VERSION', 'abaco', True),
#                           ('XTERM', 'localhost', False),
#                           ('JUPYTERHUB_USER', 'jupyter', True)])
# def test_direct_abs_path_runtimes(agave, runtime, system_id, path, result):
#     pass
