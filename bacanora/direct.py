import os
import datetime
import shutil
from . import runtimes
from . import logger as loggermodule

logger = loggermodule.get_logger(__name__)

class DirectOperationFailed(Exception):
    pass

class UnknownRuntime(DirectOperationFailed):
    pass

class UnknownStorageSystem(DirectOperationFailed):
    pass

class StorageSystems():
    prefixes = {'data-sd2e-community': {'hpc': '/work2/projects/SD2E-Community/prod/data',
                                        'abaco': '/work2/projects/SD2E-Community/prod/data',
                                        'jupyter': os.path.join(
                                            os.path.expanduser('~'), 'sd2e-community')}}

def abs_path(agave_file_path, system_id='data-sd2e-community'):
    logger.debug('agave_file_path: {}'.format(agave_file_path))
    environ = runtimes.detect()
    prefix = get_prefix(system_id, environ)
    if agave_file_path.startswith('/'):
        agave_file_path = agave_file_path[1:]
    full_path = os.path.join(prefix, agave_file_path)
    logger.debug('abs_path: {}'.format(full_path))
    return full_path

def get_prefix(storage_system, environment):
    try:
        return StorageSystems.prefixes[storage_system][environment]
    except KeyError:
        raise UnknownStorageSystem(
            'Bacanora mapping for {} is not defined'.format(storage_system))

def get(file_to_download, local_filename, system_id='data-sd2e-community'):
    try:
        full_path = abs_path(file_to_download)
        temp_local_filename = local_filename + '-' + str(int(datetime.datetime.utcnow().timestamp()))
        logger.debug('DIRECT_GET: {}'.format(full_path))
        if os.path.exists(full_path):
            shutil.copy(full_path, temp_local_filename)
        else:
            raise DirectOperationFailed('Remote source does not exist')
        try:
            os.rename(temp_local_filename, local_filename)
        except Exception as rexc:
            raise DirectOperationFailed('Atomic rename failed after download', rexc)
    except UnknownRuntime as uexc:
        raise UnknownRuntime(uexc)
    except UnknownStorageSystem as ustor:
        raise UnknownStorageSystem(ustor)

def put(file_to_upload, destination_path, system_id='data-sd2e-community'):
    try:

        full_dest_path = abs_path(destination_path)
        filename = os.path.basename(file_to_upload)
        filename_atomic = filename + '-' + str(int(datetime.datetime.utcnow().timestamp()))
        atomic_dest_path = os.path.join(full_dest_path, filename_atomic)
        final_dest_path = os.path.join(full_dest_path, filename)
        logger.debug('DIRECT_PUT: {}'.format(atomic_dest_path))
        if os.path.exists(full_dest_path):
            shutil.copy(file_to_upload, atomic_dest_path)
        else:
            raise DirectOperationFailed('Remote destination does not exist')
        try:
            os.rename(atomic_dest_path, final_dest_path)
        except Exception as exc:
            raise DirectOperationFailed('Atomic rename failed after upload', exc)
    except UnknownRuntime as uexc:
        raise UnknownRuntime(uexc)
    except UnknownStorageSystem as ustor:
        raise UnknownStorageSystem(ustor)

def exists(path_to_test, system_id='data-sd2e-community'):
    full_dest_path = abs_path(path_to_test)
    try:
        if os.path.exists(full_dest_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unhandled failure with os.path.exists()')

def isfile(path_to_test, system_id='data-sd2e-community'):
    full_dest_path = abs_path(path_to_test)
    try:
        if os.path.isfile(full_dest_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unhandled failure with os.path.isdir()')

def isdir(path_to_test, system_id='data-sd2e-community'):
    full_dest_path = abs_path(path_to_test)
    try:
        if os.path.isdir(full_dest_path):
            return True
        else:
            return False
    except Exception:
        raise DirectOperationFailed('Unhandled failure with os.path.isdir()')

def mkdir(path_to_make, system_id='data-sd2e-community'):
    full_dest_path = abs_path(path_to_make)
    try:
        os.makedirs(full_dest_path)
        return True
    except Exception:
        raise DirectOperationFailed('Exception encountered with os.makedirs()')

def delete(path_to_rm, system_id='data-sd2e-community', recursive=True):
    full_dest_path = abs_path(path_to_rm)
    try:
        if os.path.isfile(full_dest_path):
            os.remove(full_dest_path)
            return True
        elif os.path.isdir(full_dest_path):
            shutil.rmtree(full_dest_path)
            return True
        else:
            raise ValueError(
                'path {} is not a file or directory'.format(path_to_rm))
    except Exception:
        raise DirectOperationFailed('Exception encountered removing path')
