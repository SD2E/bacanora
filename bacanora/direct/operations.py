# Methods
__all__ = ['get', 'put', 'exists', 'isfile', 'isdir']

from .download import get
from .stat import exists, isfile, isdir
from .upload import put
