import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = ['MAX_SYNC_ELAPSED_FILES', 'MAX_SYNC_ELAPSED_ABACO']

# Maximum time allowed for synchronous file operations (seconds)
MAX_SYNC_ELAPSED_FILES = int(
    os.environ.get('BACANORA_MAX_SYNC_ELAPSED_FILES', '3600'))

# Maximum time allowed for synchronous actor execution (seconds)
MAX_SYNC_ELAPSED_ABACO = int(
    os.environ.get('BACANORA_MAX_SYNC_ELAPSED_ABACO', '3600'))
