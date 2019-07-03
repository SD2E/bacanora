"""
Helper functions for common filesystem operations with Agave
"""
import os
import re
import time
from random import random
from agavepy.agave import Agave, AgaveError
from requests.exceptions import HTTPError

PWD = os.getcwd()
MAX_ELAPSED = 300
MAX_RETRIES = 5
DELAY = 1
MULTIPLIER = 2


def agave_upload_file(agaveClient,
                      agaveDestPath,
                      systemId,
                      uploadFile,
                      sync=True,
                      timeOut=MAX_ELAPSED):
    """
    Upload a file to Agave-managed remote storage.

    If sync is True, the function will wait for the upload to
    complete before returning. Raises exceptions on importData
    or timeout errors.
    """
    # NOTE: I know a hack to fix the issue with in-place overwrites not having
    # the proper terminal state. It should also increase the atomicity of the
    # uploads process. Upload to a namespaced path (agaveDestPath.tmp), track
    # that file, then do a mv operation at the end. Formally, its no differnt
    # for provenance than uploading in place.
    try:
        agaveClient.files.importData(
            systemId=systemId,
            filePath=agaveDestPath,
            fileToUpload=open(uploadFile))
    except HTTPError as h:
        http_err_resp = read_tapis_http_error(h)
        raise Exception(http_err_resp)
    except Exception as e:
        raise Exception("Unknown error uploading {}: {}".format(uploadFile, e))

    uploaded_filename = os.path.basename(uploadFile)
    if sync:
        fullAgaveDestPath = os.path.join(agaveDestPath, uploaded_filename)
        wait_for_file_status(agaveClient, fullAgaveDestPath, systemId, timeOut)

    return True


def wait_for_file_status(agaveClient,
                         agaveWatchPath,
                         systemId,
                         maxTime=MAX_ELAPSED):
    """
    Synchronously wait for a file's status to reach a terminal state.

    Returns an exception and the final state if it timeout is exceeded. Uses
    exponential backoff to avoid overloading the files server with poll
    requests. Returns True on success.
    """

    # Note: This is not reliable if a lot of actions are taken on the
    #       file, such as serially re-uploading it, granting pems, etc
    #       because history is not searchable nor does it distinguish
    #       between terminal physical states (done uploading) and
    #       emphemeral actions (pems grants, downloads, etc). A reliable
    #       implementation might spawn a temporary callback channel
    #       (i.e. requestbin) subscribed to only terminal events, then
    #       monitor its messages to watch for completion.
    TERMINAL_STATES = [
        'STAGING_COMPLETED', 'TRANSFORMING_COMPLETED', 'CREATED', 'DOWNLOAD'
    ]

    assert maxTime > 0
    assert maxTime <= 1000

    delay = 0.150  # 300 msec
    expires = (time.time() + maxTime)
    stat = None

    while (time.time() < expires):
        try:
            hist = agaveClient.files.getHistory(
                systemId=systemId, filePath=agaveWatchPath)
            stat = hist[-1]['status']
            if stat in TERMINAL_STATES:
                return True
        except Exception:
            # we have to swallow this exception because status isn't available
            # until the files service picks up the task. sometimes that's
            # immediate and sometimes it's backlogged - we dont' want to fail
            # just because it takes a few seconds or more before status becomes
            # available since we went through the trouble of setting up
            # exponential backoff!
            pass

        time.sleep(delay)
        delay = (delay * (1 + random()))

    raise Exception(
        "Status transition for {} exceeded {} sec. Last status: {}".format(
            agaveWatchPath, maxTime, stat))
