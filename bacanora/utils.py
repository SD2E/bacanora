"""Top-level helper functions for generating time stamps,
manipulating paths, importing modules on demand, and much more.
"""
from deprecated.sphinx import deprecated, versionadded
import os
import datetime
import importlib
import re

__all__ = [
    'current_time', 'normpath', 'normalize', 'rooted_path', 'microseconds',
    'nanoseconds'
]


@versionadded(version='1.0.0', reason="First release")
def current_time():
    """Current UTC time
    Returns:
        A ``datetime`` object rounded to millisecond precision
    """
    return datetime.datetime.fromtimestamp(
        int(datetime.datetime.utcnow().timestamp() * 1000) / 1000)


@versionadded(version='1.0.0', reason="First release")
def microseconds():
    """Current time in microseconds as ``int``
    """
    return int(round(datetime.datetime.utcnow().timestamp() * 1000 * 1000))


@versionadded(version='1.0.0', reason="First release")
def nanoseconds():
    """Current time in nanoseconds as ``int``
    """
    return int(
        round(datetime.datetime.utcnow().timestamp() * 1000 * 1000 * 1000))


@versionadded(version='1.0.0', reason="First release")
def normalize(file_path):
    """Trim leading slash or slashes from a path

    Args:
        file_path (str): Path to normalize

    Returns:
        str: Normalized file_path
    """
    fp = re.sub('^(/)+', '', file_path)
    fp = re.sub('(/)+$', '', fp)
    return fp


@versionadded(version='1.0.0', reason="First release")
def normpath(file_path):
    """Collapse duplicate leading slashes and resolve relative references
    in a path

    Args:
        file_path (str): Path to process

    Returns:
        str: Processed file_path
    """
    fp = re.sub('^(/)+', '/', file_path)
    if not fp.startswith('/'):
        fp = '/' + fp
    fp = re.sub('(/)+$', '', fp)
    return os.path.normpath(fp)


@versionadded(version='1.0.0', reason="First release")
def rooted_path(file_path, root_dir='/'):
    """Safely combine a relative (which might not actually
    be relative) and base path.

    Args:
        file_path (str): Relative path
        root_dir (str, optional): Base path for file_path

    Returns:
        str: Processed file_path
    """
    return os.path.join(root_dir, normalize(file_path))


def dynamic_import(module, package=None):
    """Dynamically import a module by name at runtime

    Args:
        module (str): The name of the module to import
        package (str, optional): The package to import ``module`` from

    Returns:
        object: The imported module
    """
    return importlib.import_module(module, package=package)
