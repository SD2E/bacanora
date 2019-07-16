"""Facades for the Tapis ``files-pems-*`` operations
"""
from deprecated.sphinx import deprecated, versionadded
from . import logger as loggermodule
from . import settings
from .tapis import pems
from .processors import process, ProcessingOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['grant']


@versionadded(version='1.0.0', reason="First release")
def grant(file_path,
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          username=pems.DEFAULT_PEM_GRANTEE,
          pem=pems.DEFAULT_PEM_LEVEL,
          recursive=False,
          permissive=True,
          agave=None):
    """Recursively grant a permission level on a path to a specific user

    This operation presentl has no POSIX-native equivalent

    Arguments:
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
        ProcessingOperationFailed: Some other error was encountered
    """
    return process(
        'grant',
        file_path=file_path,
        system_id=system_id,
        root_dir=root_dir,
        username=username,
        pem=pem,
        recursive=recursive,
        permissive=permissive,
        agave=agave)
