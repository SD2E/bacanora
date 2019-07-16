"""Implements POSIX-native implementations of S3 files operations

The ``s3`` submodule takes advantage of native filesystem mounts to support
lightning-fast transfers from S3 to Tapis-managed storageSystems running on
TACC hosts.
"""
from .exceptions import *
from .operations import *
from .system import (s3_runtime_bases)
from .bucket import (s3_to_tapis, from_s3_uri, to_s3_uri,
                     system_props_from_bucket)
