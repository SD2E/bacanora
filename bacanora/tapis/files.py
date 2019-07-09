from .. import settings

FILE_TYPES = ('file')
DIRECTORY_TYPES = ('dir')
FILES_TYPES = FILE_TYPES + DIRECTORY_TYPES

TYPE_KEY = 'type'
NAME_KEY = 'name'
PATH_KEY = 'path'

PAGE_SIZE = settings.FILES_LIST_PAGESIZE

__all__ = [
    'FILES_TYPES', 'FILE_TYPES', 'DIRECTORY_TYPES', 'TYPE_KEY', 'NAME_KEY',
    'PATH_KEY', 'PAGE_SIZE'
]
