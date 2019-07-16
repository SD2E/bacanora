import os
import pytest

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/runtimes')

from bacanora import runtimes


@pytest.mark.parametrize("string_value, test_pass", [('abaco', True),
                                                     ('Abaco', True),
                                                     ('jupyter', True),
                                                     ('jupyter_hpc', False),
                                                     ('hpc_jupyter', True),
                                                     ('deadbeef', False),
                                                     (None, False)])
def test_init_runtime_class(string_value, test_pass):
    """BacanoraRuntime values are restricted
    """
    if test_pass:
        runtimes.BacanoraRuntime(string_value)
    else:
        with pytest.raises(ValueError):
            runtimes.BacanoraRuntime(string_value)


def test_detect_localhost(localhost_runtime):
    detected = runtimes.detect(permissive=False)
    assert detected == runtimes.LOCALHOST, 'Detected {}'.format(detected)


def test_detect_abaco(abaco_runtime):
    detected = runtimes.detect(permissive=False)
    assert detected == runtimes.ABACO, 'Detected {}'.format(detected)


def test_detect_jupyter(jupyter_runtime):
    detected = runtimes.detect(permissive=False)
    assert detected == runtimes.JUPYTER, 'Detected {}'.format(detected)


def test_detect_hpc_jupyter(hpc_jupyter_runtime):
    detected = runtimes.detect(permissive=False)
    assert detected == runtimes.HPC_JUPYTER, 'Detected {}'.format(detected)


def test_detect_hpc(hpc_runtime):
    detected = runtimes.detect(permissive=False)
    assert detected == runtimes.HPC, 'Detected {}'.format(detected)


def test_detect_failed():
    with pytest.raises(runtimes.RuntimeNotDetected):
        runtimes.detect(permissive=False)


# @pytest.mark.parametrize("env_var, runtime, test_pass",
#                          [('REACTORS_VERSION', 'abaco', True),
#                           ('XTERM', 'localhost', False),
#                           ('JUPYTERHUB_USER', 'jupyter', True)])
# def test_detect(monkeypatch, env_var, runtime, test_pass):
#     """Detecting runtime by ENV content
#     """
#     monkeypatch.setenv(env_var, 'meep')
#     if test_pass:
#         detected = runtimes.detect(permissive=False)
#         assert detected == runtime
#     else:
#         with pytest.raises(runtimes.RuntimeNotDetected):
#             runtimes.detect(permissive=False)
