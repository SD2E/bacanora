"""Tapis implementations of ``walk`` and ``listdir`` based on
recursive ``files-list`` operations
"""
import copy
import os
import shutil
from ..logger import get_logger
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath, rooted_path
from .stat import exists
from ..exceptions import HTTPError, AgaveError
from .exceptions import TapisOperationFailed
from .utils import read_tapis_http_error
from . import files
from tenacity import (retry, retry_if_exception_type, stop_after_delay,
                      wait_exponential)

logger = get_logger(__name__)

__all__ = ['walk', 'listdir']

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM
DEFAULT_PAGE_SIZE = files.PAGE_SIZE


# Wrapping the core files-list function, which is called recursively by
# walk() and listdir(), with @retry prevents a single missed/errored API call
# from forcing the system to restart a possibly very expensive recursive
# directory tree traversal
@retry(
    retry=retry_if_exception_type(AgaveError),
    reraise=True,
    stop=stop_after_delay(8),
    wait=wait_exponential(multiplier=2, max=64))
def _files_list(directory_path,
                system_id=DEFAULT_SYSTEM_ID,
                limit=DEFAULT_PAGE_SIZE,
                offset=0,
                root_dir='/',
                agave=None):
    """Private function to resiliently list a Tapis files directory
    """
    rooted_directory_path = rooted_path(directory_path, root_dir)
    logger.info('_files_list: agave://{}{}'.format(system_id, directory_path))
    try:
        return agave.files.list(
            systemId=system_id,
            filePath=rooted_directory_path,
            limit=limit,
            offset=offset)
    except Exception as err:
        logger.warning('_files_list.error: {}'.format(err))
        raise


def _walk(directory_path,
          current_listing=[],
          system_id=DEFAULT_SYSTEM_ID,
          root_dir='/',
          directories=False,
          dotfiles=False,
          page_size=DEFAULT_PAGE_SIZE,
          recurse=True,
          sort=False,
          agave=None):
    """Private function implementing an analogue to os.walk()
    """
    logger.info('_walk: agave://{}{}'.format(system_id, directory_path))
    # If current_listing is not cloned, it will grow without bounds each
    # time _walk is called. This is undocumented behavior as far as I can
    # tell from the Python docs
    listing = copy.copy(current_listing)
    logger.info('_walk: current_listing has {} elements'.format(len(listing)))
    keeplisting = True
    skip = 0
    while keeplisting:
        sublist = _files_list(
            directory_path,
            system_id=system_id,
            root_dir='/',
            limit=page_size,
            offset=skip,
            agave=agave)
        logger.debug('_walk: sublist has {} elements'.format(len(sublist)))
        skip = skip + page_size
        if len(sublist) < page_size:
            keeplisting = False
            logger.debug('_walk: recursion has ended')
        for f in sublist:
            if f[files.NAME_KEY] != '.':
                exclude_dotfile = f[files.NAME_KEY].startswith('.') \
                    and dotfiles is False
                if f[files.TYPE_KEY] in \
                        files.FILE_TYPES or directories is True:
                    if not exclude_dotfile:
                        listing.append(f[files.PATH_KEY])
                # Recurse into found directories
                if f[files.
                     TYPE_KEY] in files.DIRECTORY_TYPES and recurse is True:
                    logger.debug('_walk: descend into {}'.format(
                        f[files.PATH_KEY]))
                    _walk(
                        f[files.PATH_KEY],
                        current_listing=listing,
                        system_id=system_id,
                        root_dir=root_dir,
                        directories=directories,
                        dotfiles=dotfiles,
                        page_size=page_size,
                        recurse=recurse,
                        agave=agave)
        if sort:
            listing.sort()
        return listing


def walk(directory_path,
         system_id=DEFAULT_SYSTEM_ID,
         root_dir='/',
         directories=False,
         dotfiles=False,
         sort=False,
         page_size=DEFAULT_PAGE_SIZE,
         agave=None):
    """Recursively list contents of a Tapis files directory.

    Args:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        page_size (int, optional): Override default Tapis files-list page size
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of Tapis-canonical absolute paths

    Raises:
       TapisOperationFailed: An exception or error happened
    """
    logger.info('walk: agave://{}{}'.format(system_id, directory_path))
    start_time = nanoseconds()

    listing = _walk(
        directory_path,
        system_id=system_id,
        root_dir=root_dir,
        directories=directories,
        dotfiles=dotfiles,
        page_size=page_size,
        agave=agave)

    if sort:
        listing.sort()

    end_time = nanoseconds()
    elapsed = int((end_time - start_time) / 1000 / 1000)
    logger.debug('walk: found {} elements in {} msec'.format(
        len(listing), elapsed))

    return listing


def listdir(directory_path,
            system_id=DEFAULT_SYSTEM_ID,
            root_dir='/',
            directories=True,
            dotfiles=False,
            page_size=DEFAULT_PAGE_SIZE,
            sort=True,
            agave=None):
    """List immediate contents of a Tapis files directory.

    Args:
        directory_path (str): Full or relative path of directory to walk
        system_id (str, optional): Tapis storageSystem for directory_path
        root_dir (str, optional): Base path if directory_path is relative
        directories (bool, optional): Whether result should include directories
        dotfiles (bool, optional): Whether result should include dotfiles
        agave (Agave, optional): Tapis (Agave) API client

    Returns:
        list: List of paths relative to directory_path

    Raises:
        TapisOperationFailed: Some error prevented the action from completing
    """
    logger.info('listdir: agave://{}{}'.format(system_id, directory_path))
    start_time = nanoseconds()

    resp = _walk(
        directory_path,
        system_id=system_id,
        root_dir=root_dir,
        directories=directories,
        dotfiles=dotfiles,
        page_size=page_size,
        recurse=False,
        agave=agave)

    # filter dirname from paths to emulate os.listdir()
    if not directory_path.endswith('/'):
        directory_path_filter = directory_path + '/'
    else:
        directory_path_filter = directory_path
    listing = [f.replace(directory_path_filter, '') for f in resp]

    if sort:
        listing.sort()

    end_time = nanoseconds()
    elapsed = int((end_time - start_time) / 1000 / 1000)
    logger.debug('listdir: found {} elements in {} msec'.format(
        len(listing), elapsed))

    return listing
