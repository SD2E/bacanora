import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = [
    'FILES_BLOCK_SIZE', 'FILES_ATOMIC_OPERATIONS', 'FILES_LIST_PAGESIZE',
    'HASHIDS_SALT', 'LOCALHOST_ROOT_DIR'
]

# Download block size
FILES_BLOCK_SIZE = int(os.environ.get('BACANORA_FILES_BLOCK_SIZE ', '4096'))

# Whether to do file operations atomically (adds overhead)
FILES_ATOMIC_OPERATIONS = parse_boolean(
    os.environ.get('BACANORA_FILES_ATOMIC_OPERATIONS', '1'))

# Deault number of entries returned in a files-list operation
FILES_LIST_PAGESIZE = int(
    os.environ.get('BACANORA_FILES_LIST_PAGESIZE ', '100'))

HASHIDS_SALT = os.environ.get('BACANORA_HASHIDS_SALT',
                              'TcJzUZKcuLn6bvrwkY8nesE3')

LOCALHOST_ROOT_DIR = os.environ.get('BACANORA_LOCALHOST_ROOT_DIR',
                                    os.path.join(os.getcwd(), 'tmp'))
