import os
import pytest
import shutil
import warnings
from bacanora import utils


def local_delete(path_to_delete):
    del_target_norm = utils.normalize(path_to_delete)
    try:
        os.unlink(del_target_norm)
    except Exception:
        warnings.warn('Failed to delete file {}'.format(del_target_norm))
        try:
            shutil.rmtree(del_target_norm)
        except Exception:
            warnings.warn('Failed to delete dir {}'.format(del_target_norm))


def remote_delete(path_to_delete, system_id, agave):
    del_target_norm = utils.normpath(path_to_delete)
    try:
        agave.files.delete(filePath=path_to_delete, storageSystem=system_id)
    except Exception:
        warnings.warn('Failed to delete file {}'.format(del_target_norm))
