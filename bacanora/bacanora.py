from .logger import get_logger
# allow processors.process() to be called directly
from . import processors

# make backends discoverable to dynamic_import()
from . import direct
from . import s3
from . import tapis

# bacanora.files.get/put/etc
from . import files

# exported exceptions
from .processors import (ProcessingOperationFailed, OperationNotImplemented,
                         BackendNotImplemented)

# legacy functions
from .compat import upload, download

logger = get_logger(__name__)
