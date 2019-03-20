import os
# from funcy import distinct, remove
from .helpers import fix_assets_path, array_from_string, parse_boolean, int_or_none, set_from_string
from .organization import *
from .callbacks import *
from .debug import *

def all_settings():
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") and not isinstance(item, ModuleType):
            settings[name] = item
    return settings

# TODO - Add code and a build target that walks settings to generate an example Dockerfile w envs

# TypedUUID
# UUID_NAMESPACE = uuid3(NAMESPACE_DNS, DNS_DOMAIN)

# Managed storage defaults
STORAGE_SYSTEM = os.environ.get(
    'BACANORA_STORAGE_SYSTEM', TACC_PRIMARY_STORAGE_SYSTEM)

# Maximum delay before marking a tenacity-wrapped call as failed
RETRY_MAX_DELAY = int(os.environ.get(
    'BACANORA_RETRY_MAX_DELAY ', '180'))

# Re-raise original exception on failure
RETRY_RERAISE = parse_boolean(os.environ.get(
    'BACANORA_RETRY_RERAISE', '1'))

LOG_LEVEL = os.environ.get('BACANORA_LOG_LEVEL', 'DEBUG')
LOG_VERBOSE = parse_boolean(os.environ.get(
    'BACANORA_LOG_VERBOSE', '1'))
