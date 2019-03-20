import os
import json
import re
import sys
import tempfile
from pprint import pformat
from attrdict import AttrDict
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from tenacity import retry, retry_if_exception_type
from tenacity import stop_after_delay
from tenacity import wait_exponential

from . import agaveutils
from . import direct
from . import logger as loggermodule
from . import settings
from .direct import DirectOperationFailed

DEFAULT_STORAGE_SYSTEM = 'data-sd2e-community'
RETRY_MAX_DELAY  = settings.RETRY_MAX_DELAY
RETRY_RERAISE = settings.RETRY_RERAISE
VERBOSE_LOGGING = settings.LOG

PWD = os.getcwd()
logger = loggermodule.get_logger(__name__)

@retry(retry=retry_if_exception_type(AgaveError), reraise=RETRY_RERAISE,
       stop=stop_after_delay(RETRY_MAX_DELAY), wait=wait_exponential(multiplier=2, max=64))
def download(agave_client, file_to_download, local_filename, system_id=DEFAULT_STORAGE_SYSTEM):
    """Implements Agave files.download

    Arguments:
        agave_client (Agave): An active Agave client
        file_to_download (str): Absolute path of file to download
        local_filename (str): Local name of file once downloaded
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
    """
    try:
        direct.get(file_to_download, local_filename, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info(pformat(exc))
        # Download using Agave API call
        try:
            downloadFileName = os.path.join(PWD, local_filename)
            # Implements atomic download
            f = tempfile.NamedTemporaryFile('wb', delete=False, dir=PWD)
            # with open(downloadFileName, 'wb') as f:
            rsp = agave_client.files.download(systemId=system_id,
                                              filePath=file_to_download)
            if isinstance(rsp, dict):
                raise AgaveError(
                    "Failed to download {}".format(file_to_download))
            for block in rsp.iter_content(2048):
                if not block:
                    break
                f.write(block)
            try:
                os.rename(f.name, downloadFileName)
            except Exception as rexc:
                raise OSError('Atomic rename failed after download', rexc)
            return downloadFileName
        except (HTTPError, AgaveError) as http_err:
            try:
                os.unlink(f.name)
            except Exception:
                pass
            if re.compile('404 Client Error').search(str(http_err)):
                raise HTTPError('404 Not Found') from http_err
            else:
                http_err_resp = agaveutils.process_agave_httperror(http_err)
                raise AgaveError(http_err_resp) from http_err

@retry(retry=retry_if_exception_type(AgaveError), reraise=RETRY_RERAISE,
       stop=stop_after_delay(RETRY_MAX_DELAY), wait=wait_exponential(multiplier=2, max=64))
def upload(agave_client, file_to_upload, destination_path,
          system_id=DEFAULT_STORAGE_SYSTEM, autogrant=False):
    """Implements Agave files.upload and optional permission grant

    Arguments:
        agave_client (Agave): An active Agave client
        file_to_upload (str): Path of file to upload
        destination_path (str): Absolute path on destination storage system
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
        autogrant (bool, optional): Whether to automatically grant world read to uploaded file [False]
    """
    try:
        direct.put(file_to_upload, destination_path, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info(pformat(exc))
        try:
            agave_client.files.importData(systemId=system_id,
                                          filePath=destination_path,
                                          fileToUpload=open(file_to_upload, 'rb'))
        except HTTPError as h:
            http_err_resp = agaveutils.process_agave_httperror(h)
            raise Exception(http_err_resp)
        except Exception as e:
            raise AgaveError(
                "Error uploading {}: {}".format(file_to_upload, e))
    if autogrant:
        return grant(agave_client, destination_path, system_id=system_id)
    else:
        return True

@retry(stop=stop_after_delay(RETRY_MAX_DELAY), reraise=RETRY_RERAISE,
       wait=wait_exponential(multiplier=2, max=64))
def grant(agave_client, pems_grant_target, system_id=DEFAULT_STORAGE_SYSTEM,
          username='world', permission='READ'):
    """Failure-resistant Agave files.pems.update

    Arguments:
        agave_client (Agave): An active Agave client
        pems_grant_target (str): Absolute path on destination storage system
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
        username (str, optional): Username to grant permission to [world]
        permission (str, optional): Permission to grant [READ]
    """
    try:
        pemBody = {'username': username,
                   'permission': permission,
                   'recursive': False}
        agave_client.files.updatePermissions(systemId=system_id,
                                             filePath=pems_grant_target,
                                             body=pemBody)
    except HTTPError as h:
        http_err_resp = agaveutils.process_agave_httperror(h)
        raise Exception(http_err_resp)
    except Exception as e:
        raise AgaveError(
            "Error setting permissions on {}: {}".format(pems_grant_target, e))
    return True

@retry(stop=stop_after_delay(RETRY_MAX_DELAY), reraise=RETRY_RERAISE,
       wait=wait_exponential(multiplier=2, max=64))
def exists(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    if direct.exists(path_to_test, system_id=system_id):
        return True
    else:
        return agaveutils.exists(agave_client, path_to_test, systemId=system_id)

@retry(stop=stop_after_delay(RETRY_MAX_DELAY), reraise=RETRY_RERAISE,
       wait=wait_exponential(multiplier=2, max=64))
def isfile(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    if direct.isfile(path_to_test, system_id=system_id):
        return True
    else:
        return agaveutils.isfile(agave_client, path_to_test, systemId=system_id)

@retry(stop=stop_after_delay(RETRY_MAX_DELAY), reraise=RETRY_RERAISE,
       wait=wait_exponential(multiplier=2, max=64))
def isdir(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    if direct.isdir(path_to_test, system_id=system_id):
        return True
    else:
        return agaveutils.isdir(agave_client, path_to_test, systemId=system_id)

@retry(stop=stop_after_delay(RETRY_MAX_DELAY), reraise=RETRY_RERAISE,
       wait=wait_exponential(multiplier=2, max=64))
def mkdir(agave_client, path_to_make, system_id=DEFAULT_STORAGE_SYSTEM):
    if isdir(agave_client, path_to_make, system_id=system_id):
        return True
    try:
        return direct.mkdir(path_to_make, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info(pformat(exc))
        return agaveutils.files.mkdir(agave_client,
                                      path_to_make,
                                      systemId=system_id)
