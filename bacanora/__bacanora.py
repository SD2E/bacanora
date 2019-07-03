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

from . import tapis
from . import direct
from . import logger as loggermodule
from . import settings
from .direct import DirectOperationFailed

DEFAULT_STORAGE_SYSTEM = 'data-sd2e-community'
RETRY_MAX_DELAY = settings.RETRY_MAX_DELAY
RETRY_RERAISE = settings.RETRY_RERAISE
FILES_BLOCK_SIZE = settings.FILES_BLOCK_SIZE

PWD = os.getcwd()
logger = loggermodule.get_logger(__name__)


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=2, max=64))
def download(agave_client,
             file_to_download,
             local_filename=None,
             system_id=DEFAULT_STORAGE_SYSTEM):
    """Download a file from Agave files API

    Arguments:
        agave_client (Agave): An active Agave client
        file_to_download (str): Absolute path of file to download
        local_filename (str): Local name of file once downloaded
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        str: Name of downloaded file
    """
    logger.info('bacanora.download()')
    # Allow for override
    if local_filename is None:
        local_filename = os.path.basename(file_to_download)

    downloadFileName = os.path.join(PWD, local_filename)

    try:
        direct.get(file_to_download, local_filename, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info('using Agave API')
        logger.debug(pformat(exc))
        # Download using Agave API call
        try:
            downloadFileName = os.path.join(PWD, local_filename)
            # Implements atomic download
            f = tempfile.NamedTemporaryFile('wb', delete=False, dir=PWD)
            # with open(downloadFileName, 'wb') as f:
            rsp = agave_client.files.download(
                systemId=system_id, filePath=file_to_download)
            if isinstance(rsp, dict):
                raise AgaveError(
                    "Failed to download {}".format(file_to_download))
            for block in rsp.iter_content(FILES_BLOCK_SIZE):
                if not block:
                    break
                f.write(block)
            try:
                os.rename(f.name, downloadFileName)
            except Exception as rexc:
                raise OSError('Atomic rename failed after download', rexc)

        except (HTTPError, AgaveError) as http_err:
            try:
                os.unlink(downloadFileName)
            except Exception:
                logger.exception(
                    'Failed to unlink {}'.format(downloadFileName))
                pass
            if re.compile('404 Client Error').search(str(http_err)):
                raise HTTPError('404 Not Found') from http_err
            else:
                http_err_resp = tapis.read_tapis_http_error(http_err)
                raise AgaveError(http_err_resp) from http_err

    return local_filename


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=RETRY_RERAISE,
    stop=stop_after_delay(RETRY_MAX_DELAY),
    wait=wait_exponential(multiplier=2, max=64))
def upload(agave_client,
           file_to_upload,
           destination_path,
           system_id=DEFAULT_STORAGE_SYSTEM,
           autogrant=False):
    """Upload a file using Agave files, with optional world:READ grant

    Arguments:
        agave_client (Agave): An active Agave client
        file_to_upload (str): Path of file to upload
        destination_path (str): Absolute path on destination storage system
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
        autogrant (bool, optional): Whether to automatically grant world read to uploaded file [False]

    Returns:
        bool: True on success
    """
    logger.info('bacanora.upload()')
    try:
        direct.put(file_to_upload, destination_path, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info('using Agave API')
        logger.debug(pformat(exc))
        try:
            agave_client.files.importData(
                systemId=system_id,
                filePath=destination_path,
                fileToUpload=open(file_to_upload, 'rb'))
        except HTTPError as h:
            http_err_resp = tapis.read_tapis_http_error(h)
            raise Exception(http_err_resp)
        except Exception as e:
            raise AgaveError("Error uploading {}: {}".format(
                file_to_upload, e))
    if autogrant:
        return grant(agave_client, destination_path, system_id=system_id)
    else:
        return True


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def grant(agave_client,
          pems_grant_target,
          system_id=DEFAULT_STORAGE_SYSTEM,
          username='world',
          permission='READ'):
    """Grant Agave file permissions

    Arguments:
        agave_client (Agave): An active Agave client
        pems_grant_target (str): Absolute path on destination storage system
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
        username (str, optional): Username to grant permission to [world]
        permission (str, optional): Permission to grant [READ]

    Returns:
        bool: True on success
    """
    logger.info('bacanora.grant()')
    logger.info('using Agave API')
    try:
        pemBody = {
            'username': username,
            'permission': permission,
            'recursive': False
        }
        agave_client.files.updatePermissions(
            systemId=system_id, filePath=pems_grant_target, body=pemBody)
    except HTTPError as h:
        http_err_resp = tapis.read_tapis_http_error(h)
        raise Exception(http_err_resp)
    except Exception as e:
        raise AgaveError("Error setting permissions on {}: {}".format(
            pems_grant_target, e))
    return True


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def exists(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Test for existence of a file or directory

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        bool: True on existence
    """
    logger.info('bacanora.exists()')
    if direct.exists(path_to_test, system_id=system_id):
        return True
    else:
        logger.info('using Agave API')
        return tapis.exists(agave_client, path_to_test, systemId=system_id)


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def isfile(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Determine if a path points to a file

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        bool: True if target is a file
    """
    logger.info('bacanora.isfile()')
    if direct.isfile(path_to_test, system_id=system_id):
        return True
    else:
        logger.info('using Agave API')
        return tapis.isfile(agave_client, path_to_test, systemId=system_id)


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def isdir(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Determine if a path points to a directory

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        bool: True if target is a directory
    """
    logger.info('bacanora.isdir()')
    if direct.isdir(path_to_test, system_id=system_id):
        return True
    else:
        logger.info('using Agave API')
        return tapis.isdir(agave_client, path_to_test, systemId=system_id)


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def mkdir(agave_client, path_to_make, system_id=DEFAULT_STORAGE_SYSTEM):
    """Make a new directory on the specified storage system

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_make (str): Agave-absolute path to create
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        bool: True on success
    """
    logger.info('bacanora.mkdir()')
    if isdir(agave_client, path_to_make, system_id=system_id):
        return True
    try:
        return direct.mkdir(path_to_make, system_id=system_id)
    except DirectOperationFailed as exc:
        logger.info('using Agave API')
        logger.debug(pformat(exc))
        return tapis.files.mkdir(
            agave_client, path_to_make, systemId=system_id)


@retry(
    stop=stop_after_delay(RETRY_MAX_DELAY),
    reraise=RETRY_RERAISE,
    wait=wait_exponential(multiplier=2, max=64))
def delete(agave_client,
           path_to_rm,
           system_id=DEFAULT_STORAGE_SYSTEM,
           recursive=True):
    """Delete a path on the specified storage system

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_rm (str): Agave-absolute path to remove
        system_id (str, optional): Storage system where file is located [data-sd2e-community]

    Returns:
        bool: True on success
    """
    logger.info('bacanora.delete()')
    if not exists(agave_client, path_to_rm, system_id=DEFAULT_STORAGE_SYSTEM):
        logger.warning('Path {} did not exist to delete!'.format(path_to_rm))
        return True
    try:
        return direct.delete(
            path_to_rm, system_id=system_id, recursive=recursive)
    except DirectOperationFailed as exc:
        logger.info('using Agave API')
        logger.debug(pformat(exc))
        return tapis.files.delete(agave_client, path_to_rm, systemId=system_id)
