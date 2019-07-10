"""Path maps on various runtimes for the accelerated S3 upload
endpoint on select Tapis storageSystems
"""
import os
from . import corral
from .. import runtimes
from ..stores import StorageSystem, UnknownStorageSystem
from ..utils import normalize, normpath
from ..logger import get_logger
logger = get_logger(__name__)

__all__ = ['S3NotSupported', 's3_runtime_bases', 's3_runtime_paths']


class S3NotSupported(UnknownStorageSystem):
    """There is no S3 upload support for the storageSystem
    """
    pass


def s3_runtime_bases(storage_system,
                     runtime=runtimes.DEFAULT_RUNTIME,
                     agave=None):
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
    if not isinstance(storage_system, StorageSystem):
        storage_system = StorageSystem(storage_system, agave=agave)
    src_dir, dest_dir = None, None
    corral_runtime_base = '/'
    try:
        bp = corral.BASEPATHS[storage_system.type]
        if bp is None:
            raise S3NotSupported(
                'Tapis system {} is not configured for S3 ingest'.format(
                    storage_system.system_id))
    except KeyError:
        raise S3NotSupported(
            'S3 imports are not supported for {}-type systems ')
    src_dir = bp.get('src').format(storage_system.system_id)

    if runtime == runtimes.ABACO:
        corral_runtime_base = corral.ABACO_BASE
    elif runtime == runtimes.HPC:
        corral_runtime_base = corral.HPC_BASE
    elif runtime == runtimes.JUPYTER:
        # corral_runtime_base = corral.JUPYTER_BASE
        raise S3NotSupported('No access to S3 backing storage')
    else:
        corral_runtime_base = storage_system.localhost_dir

    src_dir = normpath(
        os.path.join(normalize(corral_runtime_base), normalize(src_dir)))
    dest_dir = normpath(
        os.path.join(
            storage_system.runtime_dir(runtime, '/'), normalize(
                bp.get('dest'))))

    return (src_dir, dest_dir)


def s3_runtime_paths(file_path,
                     storage_system,
                     runtime=runtimes.DEFAULT_RUNTIME,
                     agave=None):
    """Returns POSIX source and destinations for a path on a Tapis
    storageSystem which is supported by dedicated TACC S3 endpoint.

    Args:
        file_path (str): A path relative root_dir on a Tapis storageSystem
        storage_system (str/StorageSystem): A Tapis storageSystem
        runtime (str, optional): A known Bacanora runtime
        agave (Agave, optional): An active Tapis API client
    Raises:

    Returns:
        tuple: (source path, destination path)
    """
    s3_paths = s3_runtime_bases(storage_system, runtime=runtime, agave=agave)
    # logger.debug('s3_paths[0]: {}'.format(s3_paths[0]))
    # logger.debug('s3_paths[1]: {}'.format(s3_paths[1]))
    # logger.debug('file_path: {}'.format(file_path))
    src_path = os.path.join(s3_paths[0], normalize(file_path))
    dest_path = os.path.join(s3_paths[1], normalize(file_path))
    return (src_path, dest_path)
