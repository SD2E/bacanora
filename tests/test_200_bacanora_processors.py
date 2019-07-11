import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

import bacanora


@pytest.mark.parametrize("processor, command, test_pass",
                         [('tapis', 'version', True),
                          ('direct', 'version', True),
                          ('direct', 'foobar', False),
                          ('tapis', 'foobar', False),
                          ('foobaz', 'version', False),
                          ('foobaz', 'foobar', False)])
def test_bacanora_processor_trap_notimplemented(agave, processor, command,
                                                test_pass):
    """Function processor.process() should recover from missing processor
    names or commands, allowing incremental implementation of functions
    in each processor, as well as allowing functions that exist in one
    processor but not another
    """

    def exceptable_code():
        bacanora.bacanora.processors.process(
            command, processor=processor, agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with (pytest.raises(bacanora.ProcessingOperationFailed)):
            exceptable_code()
