"""Package-level helper functions for time stamping, path
manipulation, importing modules on demand, and more
"""
import os
import datetime
import importlib
import re

__all__ = [
    'current_time', 'normpath', 'normalize', 'rooted_path', 'microseconds',
    'nanoseconds'
]


def current_time():
    """Current UTC time
    Returns:
        A ``datetime`` object rounded to millisecond precision
    """
    return datetime.datetime.fromtimestamp(
        int(datetime.datetime.utcnow().timestamp() * 1000) / 1000)


def microseconds():
    """Current time in microseconds as ``int``
    """
    return int(round(datetime.datetime.utcnow().timestamp() * 1000 * 1000))


def nanoseconds():
    """Current time in nanoseconds as ``int``
    """
    return int(
        round(datetime.datetime.utcnow().timestamp() * 1000 * 1000 * 1000))


def normalize(filepath):
    """Trim leading slash or slashes from a path
    """
    fp = re.sub('^(/)+', '', filepath)
    fp = re.sub('(/)+$', '', fp)
    return fp


def normpath(filepath):
    """Collapse duplicate leading slashes and resolve relative references
    in a path
    """
    fp = re.sub('^(/)+', '/', filepath)
    if not filepath.startswith('/'):
        filepath = '/' + filepath
    fp = re.sub('(/)+$', '', fp)
    return os.path.normpath(fp)


def rooted_path(file_path, root_dir='/'):
    """Safely combine a relative (which might not actually
    be relative) and base path.
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
