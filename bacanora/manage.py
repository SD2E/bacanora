"""Facades for Tapis ``files-[manage]`` operations
"""
from . import logger as loggermodule
from . import settings
from .processors import process, ProcessingOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['mkdir', 'copy', 'rename', 'move', 'delete']


def mkdir(path_to_make,
          system_id=DEFAULT_SYSTEM_ID,
          force=False,
          root_dir='/',
          permissive=False,
          agave=None):
    """Make a directory on a Tapis storageSystem

    Emulates Python ``os.makedirs()``

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
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'mkdir',
        path_to_make=path_to_make,
        system_id=system_id,
        root_dir=root_dir,
        force=force,
        permissive=permissive,
        agave=agave)


def copy(path_to_copy,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         root_dir='/',
         permissive=False,
         agave=None):
    """Copy a file or directory to another destination on a Tapis storageSystem

    Implements a context-sensitive hybrid of Python ``shutil.copy2()``
    and ``shutil.copytree()``

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
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'copy',
        path_to_copy=path_to_copy,
        destination_path=destination_path,
        system_id=system_id,
        force=force,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def rename(path_to_rename,
           new_path_name,
           system_id=DEFAULT_SYSTEM_ID,
           force=False,
           root_dir='/',
           permissive=False,
           agave=None):
    """Rename a file or folder on a Tapis storageSystem

    Emulates Python ``os.rename()``

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
    return process(
        'rename',
        path_to_copy=path_to_rename,
        destination_path=new_path_name,
        system_id=system_id,
        force=force,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def move(path_to_move,
         destination_path,
         system_id=DEFAULT_SYSTEM_ID,
         force=False,
         root_dir='/',
         permissive=False,
         agave=None):
    """Move a file or directory to another destination on a Tapis storageSystem

    Emulates a **move** command using an implementation of Python ``os.rename()``

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
    return process(
        'move',
        path_to_copy=path_to_move,
        destination_path=destination_path,
        system_id=system_id,
        force=force,
        root_dir=root_dir,
        permissive=permissive,
        agave=agave)


def delete(path_to_delete,
           system_id=DEFAULT_SYSTEM_ID,
           root_dir='/',
           force=False,
           recursive=True,
           permissive=False,
           agave=None):
    """Delete a file or directory from a Tapis storageSystem

    Implements a context-sensitive hybrid of Python ``os.remove()``
    and ``shutil.rmtree()``

    Args:
        path_to_delete (str): Path on the storageSystem to delete
        system_id (str, optional): Tapis storageSystem to act upon
        root_dir (str, optional): Base directory if path_to_delete is relative
        permissive (bool, optional): Whether to return False or raise an Exception on failure
        agave (Agave): An active Tapis (Agave) API client

    Returns:
        bool: True on success, False on failure if permissive=True

    Raises:
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'delete',
        path_to_make=path_to_delete,
        system_id=system_id,
        root_dir=root_dir,
        force=force,
        permissive=permissive,
        agave=agave)
