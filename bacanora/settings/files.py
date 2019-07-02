import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = ['FILES_BLOCK_SIZE', 'FILES_ATOMIC_OPERATIONS']

# Download block size
FILES_BLOCK_SIZE = int(os.environ.get('BACANORA_FILES_BLOCK_SIZE ', '4096'))

# Whether to do file operations atomically (adds overhead)
FILES_ATOMIC_OPERATIONS = parse_boolean(
    os.environ.get('BACANORA_FILES_ATOMIC_OPERATIONS', '1'))
