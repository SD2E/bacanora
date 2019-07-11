"""Support for mapping Tapis storageSystems to their corresponding
TACC S3 resources and paths
"""
import os
from . import corral
from .exceptions import (S3NotSupported, S3OperationFailed)
from .. import runtimes
from .. import settings
from ..stores import StorageSystem, system_type_and_name
from ..utils import normalize, normpath
from ..logger import get_logger
logger = get_logger(__name__)

__all__ = [
    's3_runtime_bases', 's3_runtime_paths', 's3_src_dir_from_system',
    's3_dest_dir_from_system', 'corral_base_from_runtime'
]


def s3_runtime_bases(storage_system, runtime=None, agave=None):
    """Returns POSIX source and destination base paths for a Tapis
    storageSystem S3 upload endpoint.

    Args:
        storage_system (str/StorageSystem): A Tapis storageSystem
        runtime (str, optional): A known Bacanora runtime
        agave (Agave, optional): An active Tapis API client
    Raises:

    Returns:
        tuple: (source path, destination path)
    """
    detected_runtime = runtimes.detect(override=runtime)
    if not isinstance(storage_system, StorageSystem):
        storage_system = StorageSystem(storage_system, agave=agave)
    src_dir, dest_dir = None, None
    corral_runtime_base = '/'
    src_dir = s3_src_dir_from_system(storage_system)
    dest_dir = s3_dest_dir_from_system(storage_system)
    corral_runtime_base = corral_base_from_runtime(detected_runtime)

    src_dir = normpath(
        os.path.join(normalize(corral_runtime_base), normalize(src_dir)))
    dest_dir = normpath(
        os.path.join(
            storage_system.runtime_dir(runtime, '/'), normalize(dest_dir)))
    return (src_dir, dest_dir)


def corral_base_from_runtime(runtime=None):
    """Resolves the Corral base path based on Bacanora runtime
    """
    detected_runtime = runtimes.detect(override=runtime)
    corral_runtime_base = None
    if detected_runtime == runtimes.ABACO:
        corral_runtime_base = corral.ABACO_BASE
    elif detected_runtime == runtimes.HPC:
        corral_runtime_base = corral.HPC_BASE
    elif detected_runtime == runtimes.JUPYTER:
        # corral_runtime_base = corral.JUPYTER_BASE
        raise S3NotSupported('Jupyter Notebooks have no direct access to S3')
    else:
        corral_runtime_base = os.environ.get('BACANORA_LOCALHOST_ROOT_DIR',
                                             os.path.join(os.getcwd(), 'temp'))
    return corral_runtime_base


def s3_src_dir_from_system(system_id):
    """Resolve TACC S3 POSIX directory from a Tapis storageSystem

    Args:
        system_id (str): Tapis storageSystem identifier

    Returns:
        str: S3 bucket source directory for the storageSystem
    """
    (system_type, system_shortname) = system_type_and_name(system_id)
    try:
        bp = corral.BASEPATHS[system_type]
        if bp is None:
            raise S3NotSupported(
                'Tapis system {} is not configured for S3 ingest'.format(
                    system_id))
    except KeyError:
        raise S3NotSupported(
            'S3 imports are not supported for {}-type systems ')
    src_dir = bp.get('src').format(system_id)
    return src_dir


def s3_dest_dir_from_system(system_id):
    """Resolve POSIX destination directory from a Tapis storageSystem
    Args:
        system_id (str): Tapis storageSystem identifier

    Returns:
        str: S3 bucket destination directory for the storageSystem
    """
    (system_type, system_shortname) = system_type_and_name(system_id)
    try:
        bp = corral.BASEPATHS[system_type]
        if bp is None:
            raise S3NotSupported(
                'Tapis system {} is not configured for S3 ingest'.format(
                    system_id))
    except KeyError:
        raise S3NotSupported(
            'S3 imports are not supported for {}-type systems ')
    dest_dir = bp.get('dest').format(system_id)
    return dest_dir


def s3_runtime_paths(file_path, storage_system, runtime=None, agave=None):
    """Returns POSIX source and destinations for a path on a Tapis
    storageSystem which is supported by dedicated TACC S3 endpoint.

    Args:
        file_path (str): A path relative root_dir on a Tapis storageSystem
        storage_system (str/StorageSystem): A Tapis storageSystem
        runtime (str, optional): Override detected Bacanora runtime
        agave (Agave, optional): An active Tapis API client
    Raises:

    Returns:
        tuple: (source path, destination path)
    """
    detected_runtime = runtimes.detect(override=runtime)
    s3_paths = s3_runtime_bases(
        storage_system, runtime=detected_runtime, agave=agave)
    # logger.debug('s3_paths[0]: {}'.format(s3_paths[0]))
    # logger.debug('s3_paths[1]: {}'.format(s3_paths[1]))
    # logger.debug('file_path: {}'.format(file_path))
    src_path = os.path.join(s3_paths[0], normalize(file_path))
    dest_path = os.path.join(s3_paths[1], normalize(file_path))
    return (src_path, dest_path)
