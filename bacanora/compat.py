"""Provides backwards-compatible interfaces.

This module provides facades allowing code written against pre-release Bacanora
to continue to function using the newly written, more robust implementations
available in the first supported release. These legacy interfaces are
easily identifiable as they feature a mandatory Agave client as their first
parameter.
"""
from deprecated.sphinx import deprecated, versionadded, versionchanged
from . import operations
from . import settings

DEFAULT_STORAGE_SYSTEM = settings.STORAGE_SYSTEM


@deprecated(version='1.0.0', reason="Use bacanora.files.put instead")
def upload(agave_client,
           file_to_upload,
           destination_path,
           system_id=DEFAULT_STORAGE_SYSTEM,
           autogrant=False):
    """Uploads a file using Agave files.

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
    return operations.put(
        file_to_upload,
        destination_path,
        system_id=system_id,
        root_dir='/',
        force=True,
        atomic=True,
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.get instead")
def download(agave_client,
             file_to_download,
             local_filename=None,
             system_id=DEFAULT_STORAGE_SYSTEM):
    """Downloads a file from Agave files API.

    Arguments:
        agave_client (Agave): An active Agave (Tapis) client
        file_to_download (str): Absolute path of file to download
        local_filename (str, optional): Local name of file once downloaded
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]

    Returns:
        str: Name of downloaded file
    """
    return operations.get(
        file_to_download,
        system_id=system_id,
        local_filename=local_filename,
        root_dir='/',
        force=False,
        atomic=True,
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.exists instead")
def exists(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Tests for existence of a file or directory.

    Arguments:
        agave_client (Agave): An active Agave (Tapis) client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]
    Returns:
        bool: True on existence
    """
    return operations.exists(
        path_to_test,
        system_id=system_id,
        permissive=False,
        root_dir='/',
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.isfile instead")
def isfile(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Determines if a path points to a file.

    Arguments:
        agave_client (Agave): An active Agave (Tapis) client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]
    Returns:
        bool: True if target is a file
    """
    return operations.isfile(
        path_to_test,
        system_id=system_id,
        root_dir='/',
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.isdir instead")
def isdir(agave_client, path_to_test, system_id=DEFAULT_STORAGE_SYSTEM):
    """Determines if a path points to a directory.

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_test (str): Agave-absolute path to test
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]
    Returns:
        bool: True if target is a directory
    """
    return operations.isdir(
        path_to_test,
        system_id=system_id,
        root_dir='/',
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.mkdir instead")
def mkdir(agave_client, path_to_make, system_id=DEFAULT_STORAGE_SYSTEM):
    """Makes a new directory on the specified storage system.

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_make (str): Agave-absolute path to create
        system_id (str, optional): Storage system where file is located [DEFAULT_STORAGE_SYSTEM]
    Returns:
        bool: True on success
    """
    return operations.mkdir(
        path_to_make,
        system_id=system_id,
        force=False,
        permissive=False,
        agave=agave_client)


@deprecated(version='1.0.0', reason="Use bacanora.files.delete instead")
def delete(agave_client,
           path_to_rm,
           system_id=DEFAULT_STORAGE_SYSTEM,
           recursive=True):
    """Deletes a path on the specified storage system.

    Arguments:
        agave_client (Agave): An active Agave client
        path_to_rm (str): Agave-absolute path to remove
        system_id (str, optional): Storage system where file is located [data-sd2e-community]
    Returns:
        bool: True on success
    """
    return operations.delete(
        path_to_rm,
        system_id=system_id,
        root_dir='/',
        permissive=False,
        force=False,
        agave=agave_client)
