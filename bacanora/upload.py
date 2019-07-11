"""Facades for the Tapis ``files-upload`` operations
"""
from . import logger as loggermodule
from . import settings
from .processors import process, ProcessingOperationFailed

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['put']


def put(file_to_upload,
        destination_path,
        system_id=DEFAULT_SYSTEM_ID,
        root_dir='/',
        force=False,
        runtime=None,
        atomic=True,
        sync=False,
        permissive=False,
        agave=None):
    """Upload a file to a location on a Tapis storageSystem

    Args:
        file_to_upload (str): Name or relative path of file to upload
        destination_path (str): Upload destination on Tapis storageSystem
        system_id (str, optional): Tapis storageSystem where upload will go
        root_dir (str, optional): Base path if destination_path is relative
        force (bool, optional): Force overwrite on storageSystem
        runtime (string, optional): Override detected Bacanora runtime
        atomic (bool, optional): Whether to upload first to a temporary file
        sync (bool, optional): Wait until the file uploads to return
        permissive (bool, optional): Whether to return False or raise Exception on error
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        bool: True on success and False on failure

    Raises:
        ProcessingOperationFailed: Some error prevented the action from completing
    """
    return process(
        'put',
        file_to_upload=file_to_upload,
        destination_path=destination_path,
        system_id=system_id,
        root_dir=root_dir,
        atomic=atomic,
        force=force,
        runtime=runtime,
        sync=sync,
        permissive=permissive,
        agave=agave)
