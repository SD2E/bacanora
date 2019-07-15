"""Facades for the Tapis ``files-list`` operations
"""
from deprecated.sphinx import deprecated, versionadded
from . import logger as loggermodule
from . import settings
from .processors import process, ProcessingOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['walk', 'listdir']


@versionadded(version='1.0.0', reason="First release")
def walk(directory_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         runtime=None,
         directories=False,
         dotfiles=False,
         agave=None):
    """Recursively list contents of a Tapis files directory.

    Emulates Python ``os.walk()``

    Args:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        runtime (string, optional): Override detected Bacanora runtime
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of Tapis-canonical absolute paths

    Raises:
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'walk',
        directory_path=directory_path,
        system_id=system_id,
        root_dir=root_dir,
        runtime=runtime,
        directories=directories,
        dotfiles=dotfiles,
        agave=agave)


@versionadded(version='1.0.0', reason="First release")
def listdir(directory_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            runtime=None,
            directories=True,
            dotfiles=False,
            agave=None):
    """List immediate contents of a Tapis files directory.

    Args:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        runtime (string, optional): Override detected Bacanora runtime
        dotfiles (bool, optional): Whether result should include dotfiles
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of paths relative to directory_path

    Raises:
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'listdir',
        directory_path=directory_path,
        system_id=system_id,
        root_dir=root_dir,
        runtime=runtime,
        directories=directories,
        dotfiles=dotfiles,
        agave=agave)
