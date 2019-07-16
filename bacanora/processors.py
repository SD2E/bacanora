"""Bacanora's pluggable command processor

Supports multiple configurable backends (direct, tapis, lustre*)
"""
from deprecated.sphinx import deprecated, versionadded
from agavepy.agave import Agave
from bacanora.exceptions import AgaveError, HTTPError
from bacanora.logger import get_logger
from bacanora.settings import RETRY_MAX_DELAY, RETRY_RERAISE
from bacanora.utils import dynamic_import
from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_exponential)

DIRECT_PROCESSOR = 'direct'
TAPIS_PROCESSOR = 'tapis'
S3_PROCESSOR = 's3'
COMMAND_PROCESSORS = (DIRECT_PROCESSOR, TAPIS_PROCESSOR)

logger = get_logger(__name__)

__all__ = [
    'process', 'ProcessingOperationFailed', 'OperationNotImplemented',
    'BackendNotImplemented', 'COMMAND_PROCESSORS'
]


class ProcessingOperationFailed(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class OperationNotImplemented(ValueError):
    pass


class BackendNotImplemented(OperationNotImplemented):
    pass


@versionadded(version='1.0.0', reason="First release")
def restore_client(agave):
    """Load an Agave client from the environment if one is not provided.
    """
    if agave is None:
        return Agave.restore()
    else:
        return agave


@versionadded(version='1.0.0', reason="First release")
@retry(
    retry=retry_if_exception_type(ProcessingOperationFailed),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=2, max=64))
def process(command, *args, **kwargs):
    """Implements multiple dispatch for processing Tapis commands using
    configurable backends.

    Arguments:
        command (str): The command to execute

    Raises:
        ProcessingOperationFailed: The operation was unsuccessful
    """
    logger.debug('Start of process({})'.format(command))
    kwargs['agave'] = restore_client(kwargs.get('agave', None))
    exceptions = list()

    # Enable one specific processor to be requested
    processor = kwargs.get('processor', None)
    try:
        del kwargs['processor']
    except KeyError:
        pass

    # Allow override of COMMAND_PROCESSORS with one specific processor name
    if processor is not None:
        procs = [str(processor)]
    else:
        procs = COMMAND_PROCESSORS

    backend_not_implemented = 0
    operation_not_implemented = 0
    for proc in procs:
        try:
            logger.debug('Trying processor {}'.format(proc))
            if proc not in COMMAND_PROCESSORS:
                backend_not_implemented = backend_not_implemented + 1
                raise BackendNotImplemented(
                    'Unknown command processor {}'.format(proc))
            mod = dynamic_import('bacanora.' + proc)
            try:
                func = getattr(mod, command)
            except Exception:
                operation_not_implemented = operation_not_implemented + 1
                raise OperationNotImplemented(
                    '{}.{} not implemented or available'.format(proc, command))
            resp = func(*args, **kwargs)
            logger.debug('Response Type: {}'.format(type(resp)))
            if isinstance(resp, Exception):
                raise Exception(resp)
            else:
                logger.debug('Result: {}'.format(resp))
                return resp
            return resp
        except HTTPError as herr:
            logger.error('HTTP error encountered: {}'.format(herr))
            raise
        except Exception as err:
            logger.error('Exception ({}) encountered: {}'.format(
                type(err), err))
            exceptions.append(err)
    logger.debug('Trying next available processor...')

    if backend_not_implemented == len(procs):
        raise BackendNotImplemented(
            'Unable to complete {} using designated backend {}'.format(
                command, processor))
    elif operation_not_implemented == len(procs):
        raise OperationNotImplemented(
            'Unable to complete {} as it is not implemented'.format(command))
    else:
        raise ProcessingOperationFailed(
            'Unable to complete {}. Last error was {}'.format(
                command, exceptions[-1]))
