"""The bacanora package provides accelerated, resilient implementations of
common Tapis API functions. These are mostly files-oriented operations, but
support for other APIs is implemented where appropriate.
"""

from . import hashable
from .bacanora import *
from .compat import (upload, download)

from .__about__ import (
    __author__,
    __commit__,
    __copyright__,
    __email__,
    __license__,
    __summary__,
    __title__,
    __uri__,
    __version__,
)

__all__ = [
    "__author__",
    "__commit__",
    "__copyright__",
    "__email__",
    "__license__",
    "__summary__",
    "__title__",
    "__uri__",
    "__version__",
]
