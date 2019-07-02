import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

from .callbacks import *
from .debug import *
from .files import *
from .organization import *
from .sync import *
from .tenacity import *


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

# Logging
LOG_LEVEL = os.environ.get('BACANORA_LOG_LEVEL', 'DEBUG')
LOG_VERBOSE = parse_boolean(os.environ.get('BACANORA_LOG_VERBOSE', '0'))
