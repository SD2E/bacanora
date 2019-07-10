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

# TODO: Support binary FIFO?

__all__ = ['send_message']

SENDER_TAGS_MAP = {
    '_abaco_actor_id': 'x_src_actor_id',
    '_abaco_execution_id': 'x_src_execution_id',
    'JOB_ID': 'x_src_job_id',
    'EVENT': 'x_src_job_event',
    '_event_uuid': 'x_external_event_id'
}


class ExecutionNotComplete(AgaveError):
    pass


def send_message(actor_id,
                 message,
                 environment={},
                 sender_tags=True,
                 sync=False,
                 permissive=True,
                 nonce=None,
                 agave=None,
                 **kwargs):
    """
    Send a message to an Abaco actor by its actor_id (or actorAlias)

    Returns execution ID. If ignoreErrors is True, this is fire-and-forget.
    Otherwise, failures raise an Exception to be handled by the caller.
    """

    # Implement backwards compatibility w Bacanora 0.0.1
    sender_tags = sender_tags or kwargs.get('senderTags', False)
    permissive = permissive or kwargs.get('ignoreErrors', False)
    nonce = nonce or getattr(agave, 'nonce', None)

    try:
        try:
            rooted_file_path = rooted_path(file_path, root_dir)
            resp = agave.files.list(
                filePath=rooted_file_path, systemId=system_id, limit=2)[0]
            return AttrDict(resp)
        except HTTPError:
            raise
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with stat#files.list()', err)
    except Exception as err:
        logger.warning(
            'Exception encountered in rsrc_exists(): {}'.format(err))
        if permissive:
            return dict()
        else:
            raise

    logger.debug('message destination: {}'.format(actor_id))

    # agave.nonce form overrides explicit passing of 'nonce' in kwargs
    if getattr(agave, 'nonce', None) is not None:
        kwargs['nonce'] = getattr(agave, 'nonce')
    if kwargs.get('nonce', None) is not None:
        logger.debug('Using Abaco nonce to send message')

    pass_envs = {}
    if sender_tags is True:
        for env in list(SENDER_TAGS_MAP.keys()):
            if os.environ.get(env):
                pass_envs[SENDER_TAGS_MAP[env]] = os.environ.get(env)

    execution = {}
    try:
        execution = agave.actors.sendMessage(
            actor_id=actor_id,
            body={'message': message},
            environment=pass_envs,
            **kwargs)
    except Exception:
        logger.exception('Failed to message {}'.format(actor_id))
        if ignoreErrors is False:
            raise

    execution_id = execution.get('executionId', None)
    logger.debug('executionId: {}'.format(execution_id))

    if sync is False:
        return execution_id
    else:
        logger.debug('Awaiting actor/exec: {} {}'.format(
            actor_id, execution_id))
        return await_actor_execution(
            agave, actor_id=actor_id, executionId=execution_id, **kwargs)


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=1, max=8))
def await_actor_execution(agave, actor_id, executionId, **kwargs):
    # agave.nonce form overrides explicit passing of 'nonce' in kwargs
    if getattr(agave, 'nonce', None) is not None:
        kwargs['nonce'] = getattr(agave, 'nonce')
    try:
        execution_resp = agave.actors.getExecution(
            actor_id=actor_id, executionId=executionId, **kwargs)
        status = execution_resp.get('status', 'UNKNOWN')
        logger.debug('status: {}'.format(status))
        if status in ['COMPLETE', 'FAILED', 'ERROR']:
            return True
        else:
            raise ExecutionNotComplete('{}:{}.status is {}'.format(
                actor_id, executionId, status))
    except Exception:
        raise
