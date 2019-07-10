"""Tapis implementations of ``files-[manage]`` operations
"""
import os
import shutil
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .stat import exists
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed
from .utils import read_tapis_http_error

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['mkdir', 'delete', 'rename', 'move', 'copy']


def mkdir(path_to_make,
          system_id=DEFAULT_SYSTEM_ID,
          force=False,
          root_dir='/',
          permissive=False,
          agave=None):
    """Wrapper for Tapis files-mkdir

    Args:
        path_to_make (str): Path on the storageSystem to make
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base directory if path_to_delete is relative
        force (bool, optional): Force overwrite of an existing file or directory
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    try:
        try:
            logger.debug('mkdir: {}'.format(path_to_make))
            path_to_make = normpath(path_to_make)
            if not force:
                if exists(
                        path_to_make,
                        system_id=system_id,
                        root_dir=root_dir,
                        agave=agave):
                    raise TapisOperationFailed(
                        'Destination {} exists. Repeat with "force=True" to overwrite'
                        .format(path_to_make))
            agave.files.manage(
                systemId=system_id,
                body={
                    'action': 'mkdir',
                    'path': path_to_make
                },
                filePath=root_dir)
            return True
        except HTTPError as h:
            http_err_resp = read_tapis_http_error(h)
            logger.error('HTTP Error: {}'.format(http_err_resp))
            raise HTTPError(http_err_resp)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage()#mkdir', err)
    except Exception:
        if permissive:
            return False
        else:
            raise


def delete(path_to_delete,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           force=False,
           recursive=True,
           permissive=False,
           agave=None):
    """Wrapper for Tapis files-delete

    Args:
        path_to_delete (str): Path on the storageSystem to delete
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base directory if path_to_delete is relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    try:
        try:
            rooted_file_path = rooted_path(path_to_delete, root_dir)
            agave.files.delete(filePath=rooted_file_path, systemId=system_id)
            return True
        except HTTPError as herr:
            if herr.response.status_code == 404:
                logger.warning(
                    'HTTP Error: {} was not found'.format(path_to_delete))
                return False
            else:
                raise HTTPError(herr)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage()#mkdir', err)
    except Exception:
        if permissive:
            return False
        else:
            raise


def move(path_to_move,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         root_dir='/',
         permissive=False,
         agave=None):
    """Wrapper for Tapis files-move

    Args:
        path_to_move (str): Path on the storageSystem to move
        destination_path (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        root_dir (str, optional): Base directory if path_to_move and destination_path are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    try:
        try:
            rooted_path_to_move = rooted_path(path_to_move, root_dir)
            rooted_destination_path = rooted_path(destination_path, root_dir)
            if rooted_path_to_move == rooted_destination_path:
                raise TapisOperationFailed(
                    'Source and destination cannot be the same')
            if exists(
                    rooted_destination_path,
                    system_id=system_id,
                    root_dir=root_dir,
                    agave=agave):
                if force:
                    logger.warn(
                        'Deleting destination {}'.format(destination_path))
                    delete(
                        rooted_destination_path,
                        system_id=system_id,
                        root_dir=root_dir,
                        permissive=False,
                        agave=agave)
                else:
                    raise TapisOperationFailed(
                        'Destination {} exists. Repeat with "force=True" to overwrite'
                        .format(destination_path))
            agave.files.manage(
                systemId=system_id,
                body={
                    'action': 'move',
                    'path': rooted_destination_path
                },
                filePath=rooted_path_to_move)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage()#move', err)
    except Exception:
        if permissive:
            return False
        else:
            raise


def rename(path_to_rename,
           new_path_name,
           system_id=DEFAULT_SYSTEM_ID,
           force=False,
           root_dir='/',
           permissive=False,
           agave=None):
    """Wrapper for Tapis files-rename

    Args:
        path_to_rename (str): Path on the storageSystem to move
        new_path_name (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        root_dir (str, optional): Base directory if path_to_rename and new_path_name are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    return move(
        path_to_rename,
        new_path_name,
        system_id=system_id,
        force=force,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def copy(path_to_copy,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         root_dir='/',
         permissive=False,
         agave=None):
    """Wrapper for Tapis files-copy

    Args:
        path_to_copy (str): Path on the storageSystem to move
        destination_path (str): destination on the storageSystem
        system_id (str, optional): Tapis storageSystem to act upon
        force (bool, optional): Force overwrite of an existing file or directory
        root_dir (str, optional): Base directory if path_to_copy and destination_path are relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        HTTPError: Underlying transport or web service error was encountered
        TapisOperationFailed: Some other error was encountered
    """
    try:
        try:
            rooted_path_to_copy = rooted_path(path_to_copy, root_dir)
            rooted_destination_path = rooted_path(destination_path, root_dir)
            if rooted_path_to_copy == rooted_destination_path:
                raise TapisOperationFailed(
                    'Source and destination cannot be the same')
            if exists(
                    rooted_destination_path,
                    system_id=system_id,
                    root_dir=root_dir,
                    agave=agave):
                if force:
                    logger.warn(
                        'Deleting destination {}'.format(destination_path))
                    delete(
                        rooted_destination_path,
                        system_id=system_id,
                        root_dir=root_dir,
                        permissive=False,
                        agave=agave)
                else:
                    raise TapisOperationFailed(
                        'Destination {} exists. Repeat with "force=True" to overwrite'
                        .format(destination_path))
            agave.files.manage(
                systemId=system_id,
                body={
                    'action': 'copy',
                    'path': rooted_destination_path
                },
                filePath=rooted_path_to_copy)
        except Exception as err:
            raise TapisOperationFailed(
                'Exception encountered with files.manage()#copy', err)
    except Exception:
        if permissive:
            return False
        else:
            raise
