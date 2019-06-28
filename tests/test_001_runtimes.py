import os
import pytest
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/runtimes')

from bacanora import runtimes


@pytest.mark.parametrize("string_value, test_pass", [('abaco', True),
                                                     ('Abaco', True),
                                                     ('deadbeef', False),
                                                     (None, False)])
def test_runtime_class(string_value, test_pass):
    """BacanoraRuntime values are restricted
    """
    if test_pass:
        runtimes.BacanoraRuntime(string_value)
    else:
        with pytest.raises(ValueError):
            runtimes.BacanoraRuntime(string_value)


@pytest.mark.parametrize("env_var, runtime, test_pass",
                         [('REACTORS_VERSION', 'abaco', True),
                          ('XTERM', 'localhost', False),
                          ('JUPYTERHUB_USER', 'jupyter', True)])
def test_detect(monkeypatch, env_var, runtime, test_pass):
    """Detecting runtime by ENV content
    """
    monkeypatch.setenv(env_var, 'meep')
    if test_pass:
        detected = runtimes.detect(permissive=False)
        assert detected == runtime
    else:
        with pytest.raises(runtimes.RuntimeNotDetected):
            runtimes.detect(permissive=False)
