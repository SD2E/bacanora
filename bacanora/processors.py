"""Generic command processor supporting configurable backends
"""
from agavepy.agave import Agave
from bacanora.utils import dynamic_import
from bacanora.logger import get_logger

DIRECT_PROCESSOR = 'direct'
TAPIS_PROCESSOR = 'tapis'
S3_PROCESSOR = 's3'
COMMAND_PROCESSORS = (DIRECT_PROCESSOR, TAPIS_PROCESSOR)

logger = get_logger(__name__)

__all__ = ['process', 'ProcessingOperationFailed']


class ProcessingOperationFailed(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


def restore_client(agave):
    """Load an Agave client from the environment if one is not provided.
    """
    if agave is None:
        return Agave.restore()
    else:
        return agave


def process(command, *args, **kwargs):
    """Implements multiple dispatch for processing Tapis commands using
    configurable backends.

    Arguments:
        command (str): The command to execute

    Raises:
        ProcessingOperationFailed: The operation was unsuccessful
    """
    kwargs['agave'] = restore_client(kwargs.get('agave', None))
    processor = kwargs.get('processor', None)
    exceptions = list()
    if processor is not None:
        procs = [str(processor)]
    else:
        procs = COMMAND_PROCESSORS
    for proc in procs:
        logger.debug('Attempting processor {}'.format(proc))
        if proc not in COMMAND_PROCESSORS:
            raise ValueError('Unknown command processor {}'.format(proc))
        try:
            mod = dynamic_import('bacanora.' + proc)
            func = getattr(mod, command)
            resp = func(*args, **kwargs)
            logger.debug('Response Type: {}'.format(type(resp)))
            if isinstance(resp, Exception):
                raise Exception(resp)
            else:
                logger.debug('Result: {}'.format(resp))
                return resp
            return resp
        except Exception as err:
            logger.error('Exception encountered')
            exceptions.append(err)
            pass
    # print(exceptions[-1])
    raise ProcessingOperationFailed(
        'Unable to complete {}. Last error was {}'.format(
            command, exceptions[-1]))