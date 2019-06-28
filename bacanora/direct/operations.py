# Methods
__all__ = [
    'get', 'put', 'exists', 'isfile', 'isdir', 'mkdir', 'delete', 'rename'
]

from .download import get
from .stat import exists, isfile, isdir
from .upload import put
from .manage import mkdir, delete, rename
