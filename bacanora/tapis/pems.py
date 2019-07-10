"""Tapis implementations of ``files-pems-*`` operations
"""
import copy
import os
import shutil
from ..logger import get_logger
from .. import hashid
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .stat import exists, isdir
from .walk import walk
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed
from .utils import read_tapis_http_error
from . import files
from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_exponential)

logger = get_logger(__name__)

__all__ = ['grant', 'DEFAULT_PEM_GRANTEE', 'DEFAULT_PEM_LEVEL']

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
DEFAULT_PEM_GRANTEE = files.DEFAULT_PEM_GRANTEE
DEFAULT_PEM_LEVEL = files.DEFAULT_PEM_LEVEL
DEFAULT_PAGE_SIZE = files.PAGE_SIZE


@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=True,
    stop=stop_after_delay(8),
    wait=wait_exponential(multiplier=2, max=64))
def _grant(
        directory_path,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        username=DEFAULT_PEM_GRANTEE,
        pem=DEFAULT_PEM_LEVEL,
        recursive_pem=False,
        # check_before_grant=False,
        permissive=True,
        agave=None):
    """Private function to resiliently apply a permissions grant
    """
    rooted_directory_path = rooted_path(directory_path, root_dir)
    try:
        # Pave the way to multithreaded permission grants by assigning a
        # distinct identifier. At present, this just helps in inspecting
        # debugging output.
        session_id = hashid.generate(rooted_directory_path, system_id,
                                     username, pem, recursive_pem)
        logger.debug('_grant: session #{}'.format(session_id))
        # TODO- Implement check_before_grant to make this impdepotent. This is
        # better for provenance and also minimizes Tapis' database writes.
        # It should also, where a recursive grant is being re-applied
        # (e.g. Bulk grant to a directory where new files have been added),
        # improve performance by ~25%. Querying a permission requires ~ 0.62s,
        # while writing a permission record requires ~0.78s. Over 1000 records,
        # that is a 158 second difference!
        start_time = nanoseconds()
        agave.files.updatePermissions(
            systemId=system_id,
            filePath=rooted_directory_path,
            body={
                'username': username,
                'permission': pem,
                'recursive': recursive_pem
            })
        end_time = nanoseconds()
        elapsed = ((end_time - start_time) / 1000 / 1000 / 1000)
        logger.debug('_grant: completed in {} sec'.format(elapsed))
        return True
    except HTTPError:
        return False
    except Exception:
        raise


def grant(file_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          username=DEFAULT_PEM_GRANTEE,
          pem=DEFAULT_PEM_LEVEL,
          recursive=False,
          permissive=True,
          agave=None):
    """Recursively grant a permission level on a path to a specific user

    Args:
        file_path (str): Target path on a storageSystem for the grant
        system_id (str, optional): Tapis storageSystem for file_path
        root_dir (str, optional): Base path if file_path is relative
        username (str, optional): TACC.cloud username granted the permission
        pem (str, optional): TACC.cloud permission to apply
        recursive (bool, optional): Apply the Tapis 'recursive' modifier to the permission
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True if the operation completes, False if not

    Raises:
        HTTPError: Underlying web service or transport error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    rooted_file_path = rooted_path(file_path, root_dir)
    logger.info('grant: {}:{} on agave://{}{}'.format(username, pem, system_id,
                                                      rooted_file_path))
    start_time = nanoseconds()
    element_count = 0
    grants_applied = 0
    try:
        if not _grant(
                rooted_file_path,
                system_id=system_id,
                root_dir=root_dir,
                username=username,
                pem=pem,
                recursive_pem=recursive,
                agave=agave):
            raise TapisOperationFailed(
                'Initial grant failed - Abandoning grant()')
        element_count = 1
        grants_applied = 1
        # Recursively process contents if directory_path is a directory
        if isdir(
                rooted_file_path,
                system_id=system_id,
                root_dir=root_dir,
                agave=agave):
            logger.debug('grant: iterate over {}'.format(rooted_file_path))
            listing = list()
            try:
                listing = walk(
                    rooted_file_path,
                    system_id=system_id,
                    root_dir=root_dir,
                    dotfiles=True,
                    directories=True,
                    agave=agave)
                logger.debug('grant: {} new targets found'.format(
                    len(listing)))
                element_count = element_count + len(listing)
            except Exception:
                raise TapisOperationFailed(
                    'Failed to list contents of {} - Abandoning grant()'.
                    format(rooted_file_path))
            errors = list()
            for file_path in listing:
                session_id = hashid.generate(file_path, system_id, username,
                                             pem, recursive)
                try:
                    resp = _grant(
                        file_path,
                        system_id=system_id,
                        root_dir=root_dir,
                        username=username,
                        pem=pem,
                        recursive_pem=recursive,
                        agave=agave)
                    if resp is True:
                        grants_applied = grants_applied + 1
                    if resp is not True:
                        logger.warning('')
                        raise TapisOperationFailed(
                            'Grant #{} processed but did not succeed'.format(
                                session_id))
                except Exception as err:
                    # Capture individual errors but do not exit
                    errors.append(err)
                    logger.error('Grant #{} failed: {}'.format(
                        session_id, err))
    except Exception:
        if permissive:
            return False
        else:
            raise

    end_time = nanoseconds()
    elapsed = int((end_time - start_time) / 1000 / 1000)
    logger.debug('grant: found/granted {}/{} targets in {} msec'.format(
        element_count, grants_applied, elapsed))

    return True


def list_user_pem(file_path,
                  system_id=DEFAULT_SYSTEM_ID,
                  root_dir='/',
                  username=files.DEFAULT_PEM_GRANTEE,
                  agave=None):
    # AgavePy does not support querying a specific user directly but
    # we can implement a direct HTTP query like so
    # curl -skL -H "Authorization: Bearer TOKEN" https://api.server/files/v2/pems/system/SYSTEM/PATH?username.eq=USERNAME
    pass
