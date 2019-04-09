"""
Functions for working with TACC Reactors
"""
import re
import os
from agavepy.agave import Agave, AgaveError

from attrdict import AttrDict
from tenacity import retry, retry_if_exception_type
from tenacity import stop_after_delay
from tenacity import wait_exponential

from .. import logger as loggermodule
from .. import settings

logger = loggermodule.get_logger(__name__)

RETRY_MAX_DELAY = settings.RETRY_MAX_DELAY
RETRY_RERAISE = settings.RETRY_RERAISE

# TODO: Support binary FIFO?


class ExecutionNotComplete(AgaveError):
    pass


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=1, max=8))
def send_message(agaveClient,
                 actorId,
                 message,
                 environment={},
                 ignoreErrors=True,
                 sync=False,
                 senderTags=True,
                 **kwargs):
    """
    Send a message to an Abaco actor by its actorId (or actorAlias)

    Returns execution ID. If ignoreErrors is True, this is fire-and-forget.
    Otherwise, failures raise an Exception to be handled by the caller.
    """
    logger.debug('message destination: {}'.format(actorId))

    # agaveClient.nonce form overrides explicit passing of 'nonce' in kwargs
    if getattr(agaveClient, 'nonce', None) is not None:
        kwargs['nonce'] = getattr(agaveClient, 'nonce')

    if kwargs.get('nonce', None) is not None:
        logger.debug('Using Abaco nonce to send message')

    SPECIAL_VARS = {
        '_abaco_actor_id': 'x_src_actor_id',
        '_abaco_execution_id': 'x_src_execution_id',
        'JOB_ID': 'x_src_job_id',
        'EVENT': 'x_src_job_event',
        '_event_uuid': 'x_external_event_id'
    }
    pass_envs = {}
    if senderTags is True:
        for env in list(SPECIAL_VARS.keys()):
            if os.environ.get(env):
                pass_envs[SPECIAL_VARS[env]] = os.environ.get(env)

    execution = {}
    try:
        execution = agaveClient.actors.sendMessage(
            actorId=actorId,
            body={'message': message},
            environment=pass_envs,
            **kwargs)
    except Exception:
        logger.exception('Failed to message {}'.format(actorId))
        if ignoreErrors is False:
            raise

    execId = execution.get('executionId', None)
    logger.debug('executionId: {}'.format(execId))

    if sync is False:
        return execId
    else:
        logger.debug('Awaiting actor/exec: {} {}'.format(actorId, execId))
        return await_actor_execution(
            agaveClient, actorId=actorId, executionId=execId, **kwargs)


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=1, max=8))
def await_actor_execution(agaveClient, actorId, executionId, **kwargs):
    # agaveClient.nonce form overrides explicit passing of 'nonce' in kwargs
    if getattr(agaveClient, 'nonce', None) is not None:
        kwargs['nonce'] = getattr(agaveClient, 'nonce')
    try:
        execution_resp = agaveClient.actors.getExecution(
            actorId=actorId, executionId=executionId, **kwargs)
        status = execution_resp.get('status', 'UNKNOWN')
        logger.debug('status: {}'.format(status))
        if status in ['COMPLETE', 'FAILED', 'ERROR']:
            return True
        else:
            raise ExecutionNotComplete('{}:{}.status is {}'.format(
                actorId, executionId, status))
    except Exception:
        raise
