import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import (processors, OperationNotImplemented,
                      BackendNotImplemented)


@pytest.mark.parametrize("processor, command, test_pass",
                         [(processors.DIRECT_PROCESSOR, 'foobar', True),
                          (processors.TAPIS_PROCESSOR, 'foobar', True)])
def test_bacanora_processor_operation_notimplemented(agave, processor, command,
                                                     test_pass):
    """Test that a known processor + unknown command is detected
    and fails quickly.
    """

    def exceptable_code():
        processors.process(command, processor=processor, agave=agave)

    if not test_pass:
        exceptable_code()
    else:
        with (pytest.raises(OperationNotImplemented)):
            exceptable_code()


@pytest.mark.parametrize("processor, command, test_pass",
                         [('s3', 'listdir', True), ('foobaz', 'version', True),
                          ('foobaz', 'foobar', True)])
def test_bacanora_processor_backend_notimplemented(agave, processor, command,
                                                   test_pass):
    """Tests whether an exception will be raised quickly if an invalid
    value processor is raised. The alternative is a long loop of retries.
    """

    def exceptable_code():
        processors.process(command, processor=processor, agave=agave)

    if not test_pass:
        exceptable_code()
    else:
        with (pytest.raises(BackendNotImplemented)):
            exceptable_code()
