"""
Functions for working with TACC Reactors
"""
import re
import os
import time
from agavepy.agave import Agave, AgaveError
from attrdict import AttrDict
from tenacity import retry, retry_if_exception_type
from tenacity import stop_after_delay
from tenacity import wait_exponential
from pprint import pprint

MAX_ELAPSED = 300
MAX_RETRIES = 5

# TODO: Support nonces
# TODO: Support sending URL parameters
# TODO: Support binary FIFO?


class ExecutionNotComplete(AgaveError):
    pass


def message_reactor(agaveClient,
                    actorId,
                    message,
                    environment={},
                    ignoreErrors=True,
                    sync=False,
                    senderTags=True,
                    timeOut=MAX_ELAPSED):
    """
    Send a message to an Abaco actor by its ID

    Returns execution ID. If ignoreErrors is True, this is fire-and-forget.
    Otherwise, failures raise an Exception to handled by the caller.
    """
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
            actorId=actorId, body={'message': message}, environment=pass_envs)
    except Exception as e:
        errorMessage = "Error messaging actor {}: {}".format(actorId, e)
        if ignoreErrors:
            pass
        else:
            raise Exception(errorMessage)

    execId = execution.get('executionId', None)

    if sync is False:
        try:
            return execId
        except Exception as e:
            errorMessage = " Message to {} failed: {}".format(actorId, e)
            if ignoreErrors:
                pass
            else:
                raise Exception(errorMessage)
    else:
        return await_execution(
            agaveClient, actorId=actorId, executionId=execId)


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=True,
    stop=stop_after_delay(60),
    wait=wait_exponential(multiplier=1, max=16))
def await_execution(agaveClient, actorId, executionId):
    try:
        execution_resp = agaveClient.actors.getExecution(
            actorId=actorId, executionId=executionId)
        pprint(execution_resp)
        status = execution_resp.get('status', 'UNKNOWN')
        if status in ['COMPLETE', 'FAILED', 'ERROR']:
            return True
        else:
            raise ExecutionNotComplete('{}:{}.status is {}'.format(
                actorId, executionId, status))
    except Exception:
        raise
