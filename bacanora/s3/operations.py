"""Configures command functions to be handled by the ``s3`` processor
"""

from .sync import (import_file)
from .stat import (exists, isfile, isdir)
