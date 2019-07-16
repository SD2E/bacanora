"""Globals and configurations pertaining to the Tapis ``files`` web service API
"""
from .. import settings

__all__ = [
    'FILES_TYPES', 'FILE_TYPES', 'DIRECTORY_TYPES', 'TYPE_KEY', 'NAME_KEY',
    'PATH_KEY', 'PAGE_SIZE', 'DEFAULT_PEM_GRANTEE', 'DEFAULT_PEM_LEVEL'
]

FILE_TYPES = ('file')
DIRECTORY_TYPES = ('dir')
FILES_TYPES = FILE_TYPES + DIRECTORY_TYPES

TYPE_KEY = 'type'
NAME_KEY = 'name'
PATH_KEY = 'path'

PAGE_SIZE = settings.FILES_LIST_PAGESIZE

DEFAULT_PEM_GRANTEE = 'world'
DEFAULT_PEM_LEVEL = 'READ'
