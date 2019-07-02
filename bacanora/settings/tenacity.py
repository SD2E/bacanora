import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = ['RETRY_MAX_DELAY', 'RETRY_RERAISE']

# Maximum delay before marking a tenacity-wrapped call as failed
RETRY_MAX_DELAY = int(os.environ.get('BACANORA_RETRY_MAX_DELAY ', '90'))

# Whether to re-raise original exception on tenacity timeout
RETRY_RERAISE = parse_boolean(os.environ.get('BACANORA_RETRY_RERAISE', '1'))
