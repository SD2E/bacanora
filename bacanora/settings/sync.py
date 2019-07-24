import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = [
    'IMPORT_DATA_MAX_ELAPSED', 'IMPORT_DATA_RETRY_DELAY',
    'MAX_SYNC_ELAPSED_ABACO'
]

# Maximum time allowed for synchronous file operations (seconds)
IMPORT_DATA_MAX_ELAPSED = int(
    os.environ.get('BACANORA_IMPORT_DATA_MAX_ELAPSED', '3600'))

IMPORT_DATA_RETRY_DELAY = int(
    os.environ.get('BACANORA_IMPORT_DATA_RETRY_DELAY', '1'))

# Maximum time allowed for synchronous actor execution (seconds)
MAX_SYNC_ELAPSED_ABACO = int(
    os.environ.get('BACANORA_MAX_SYNC_ELAPSED_ABACO', '3600'))
