import os
# from funcy import distinct, remove
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

from .organization import *
from .callbacks import *
from .debug import *


def all_settings():
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") and not isinstance(
                item, ModuleType):
            settings[name] = item
    return settings


# TODO - Add code and a build target that walks settings to generate an example Dockerfile w envs

# Managed storage defaults
STORAGE_SYSTEM = os.environ.get('BACANORA_STORAGE_SYSTEM',
                                TACC_PRIMARY_STORAGE_SYSTEM)

# Maximum delay before marking a tenacity-wrapped call as failed
RETRY_MAX_DELAY = int(os.environ.get('BACANORA_RETRY_MAX_DELAY ', '90'))

# Whether to re-raise original exception on tenacity timeout
RETRY_RERAISE = parse_boolean(os.environ.get('BACANORA_RETRY_RERAISE', '1'))

# Logging
LOG_LEVEL = os.environ.get('BACANORA_LOG_LEVEL', 'DEBUG')
LOG_VERBOSE = parse_boolean(os.environ.get('BACANORA_LOG_VERBOSE', '0'))

# Download block size
FILES_BLOCK_SIZE = int(os.environ.get('BACANORA_FILES_BLOCK_SIZE ', '4096'))

# Whether to do file operations atomically (adds overhead)
FILES_ATOMIC_OPERATIONS = parse_boolean(
    os.environ.get('BACANORA_FILES_ATOMIC_OPERATIONS', '1'))
