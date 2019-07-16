"""Implements POSIX-native implementations of Tapis files operations.

The ``direct`` submodule takes advantage of native filesystem mounts on
TACC-hosted Tapis storageSystems to provide greatly accelerated file
operations, especially when working with large numbers of paths.
"""
from .utils import abs_path, abspath_to_tapis
from .exceptions import *
from .operations import *
