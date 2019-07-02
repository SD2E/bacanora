import os
import shutil
from agavepy.agave import AgaveError
from requests.exceptions import HTTPError
from .. import logger as loggermodule
from .. import settings
from ..utils import nanoseconds, microseconds, normalize, normpath
from ..stores import ManagedStoreError
from .exceptions import TapisOperationFailed
from .utils import process_agave_httperror

logger = loggermodule.get_logger(__name__)

DEFAULT_SYSTEM_ID = settings.STORAGE_SYSTEM

__all__ = ['put']


def put():
    pass
