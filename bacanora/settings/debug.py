import os
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

__all__ = ['DEBUG_MODE']

DEBUG_MODE = parse_boolean(
    os.environ.get('LOCALONLY', os.environ.get('DEBUG', '0')))
"""int: Global setting that allows debugging behavior to be activated.
Set by variable ``LOCALONLY``, followed by ``DEBUG``.
Default is ``0`` (**False**)
"""
