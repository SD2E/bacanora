"""Provides backwards-compatible interfaces for select Bacanora functions
"""
from deprecated.sphinx import deprecated, versionadded, versionchanged
from .operations import get, put
from . import settings

DEFAULT_STORAGE_SYSTEM = settings.STORAGE_SYSTEM


@deprecated(version='1.0.0', reason="Use bacanora.files.put instead")
def upload(agave_client,
           file_to_upload,
           destination_path,
           system_id=DEFAULT_STORAGE_SYSTEM,
           autogrant=False):
    """Upload a file using Agave files, with optional world:READ grant
    Arguments:
        agave_client (Agave): An active Agave (Tapis) client
        file_to_upload (str): Path of file to upload
        destination_path (str): Absolute path on destination storage system
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]
        autogrant (bool, optional): Whether to automatically grant world read to uploaded file [False]

    Returns:
        bool: True on success
    """
    if autogrant:
        raise NotImplementedError(
            'The "autogrant" option is no longer supported')
    return put(
        file_to_upload,
        destination_path,
        system_id=system_id,
        force=True,
        atomic=True,
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.get instead")
def download(agave_client,
             file_to_download,
             local_filename=None,
             system_id=DEFAULT_STORAGE_SYSTEM):
    """Download a file from Agave files API
    Arguments:
        agave_client (Agave): An active Agave (Tapis) client
        file_to_download (str): Absolute path of file to download
        local_filename (str, optional): Local name of file once downloaded
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]

    Returns:
        str: Name of downloaded file
    """
    return get(
        file_to_download,
        system_id=system_id,
        local_filename=local_filename,
        force=False,
        atomic=True,
        permissive=False,
        agave=agave_client)
