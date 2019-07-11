import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/tapis')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import tapis
from .utils import remote_delete


@pytest.mark.parametrize(
    "file_path, system_id, force_action, test_pass, last_test",
    [('/sample/tacc-cloud/test-mkdir', 'data-sd2e-community', True, True,
      False),
     ('/sample/tacc-cloud/test-mkdir', 'data-sd2e-community', False, False,
      False),
     ('/sample/tacc-cloud/test-mkdir', 'data-sd2e-community', True, True,
      True),
     ('/sample/tacc-cloud/test-mkdir-1/', 'data-sd2e-community', True, True,
      False),
     ('/sample/tacc-cloud/test-mkdir-1/', 'data-sd2e-community', False, False,
      False),
     ('/sample/tacc-cloud/test-mkdir-1/', 'data-sd2e-community', True, True,
      True),
     ('/sample/tacc-cloud/test-mkdir-1/', 'data-projects-fake-project', True,
      False, True)])
def test_tapis_manage_mkdir(agave, file_path, system_id, force_action,
                            test_pass, last_test):
    """Tapis mkdir can create a path, refusing to overwrite
    unless force=True
    """

    def exceptable_code():
        tapis.mkdir(
            file_path, system_id=system_id, force=force_action, agave=agave)
        listing = agave.files.list(filePath=file_path, systemId=system_id)
        files = [tapis.utils.normpath(f.get('path')) for f in listing]
        assert tapis.utils.normpath(file_path) in files

    if test_pass:
        exceptable_code()
        if last_test:
            try:
                remote_delete(file_path, system_id, agave)
            except Exception:
                raise
                # warnings
    else:
        with pytest.raises(Exception):
            exceptable_code()

    # if last_test:
    #     try:
    #         remote_delete(file_path, system_id, agave)
    #     except Exception:
    #         raise
    #         # warnings.warn('Failed to delete {}'.format(file_path))


@pytest.mark.parametrize(
    "file_path, system_id, destination_path, force_action, test_pass",
    [('/sample/tacc-cloud/README.rst', 'data-sd2e-community',
      '/sample/tacc-cloud/README-copy-1.rst', True, True),
     ('/sample/tacc-cloud/README.rst', 'data-sd2e-community',
      '/sample/tacc-cloud/README-copy-2.rst', True, True),
     ('/sample/tacc-cloud/README.rst', 'data-sd2e-community',
      '/sample/tacc-cloud/README-copy-1.rst', False, True),
     ('/sample/tacc-cloud/README.rst', 'data-sd2e-community',
      '/sample/tacc-cloud/README-copy-1.rst', True, True),
     ('/sample/tacc-cloud/README.rst', 'data-sd2e-fakesystem',
      '/sample/tacc-cloud/README-copy-1.rst', True, False),
     ('/sample/tacc-cloud/agavehelpers', 'data-sd2e-community',
      '/sample/tacc-cloud/agavehelpers-copy', True, True),
     ('/sample/tacc-cloud/agavehelpers', 'data-sd2e-community',
      '/sample/tacc-cloud/agavehelpers-copy', False, False)])
def test_tapis_manage_copy(agave, file_path, system_id, destination_path,
                           force_action, test_pass):
    """Tapis copy can rename a path on the given storageSystem, refusing
    to overwrite unless force=True
    """

    def exceptable_code():
        tapis.copy(
            file_path,
            destination_path,
            system_id=system_id,
            force=force_action,
            agave=agave)
        listing = agave.files.list(
            filePath=os.path.dirname(file_path), systemId=system_id)
        files = [tapis.utils.normpath(f.get('path')) for f in listing]
        if not tapis.utils.normpath(destination_path) in files:
            raise FileNotFoundError()

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()


@pytest.mark.parametrize(
    "src_file_path, file_path, system_id, destination_path, force_action, test_pass",
    [('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-copy-2.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-copy-3.rst', True,
      True),
     ('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-copy-2.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-copy-3.rst', False,
      False),
     ('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-copy-2.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-copy-3.rst', True,
      True)])
def test_tapis_manage_rename(agave, src_file_path, file_path, system_id,
                             destination_path, force_action, test_pass):
    """Tapis copy can rename a path on the given storageSystem, refusing
    to overwrite unless force=True
    """

    def exceptable_code():
        tapis.copy(
            src_file_path,
            file_path,
            system_id=system_id,
            force=True,
            agave=agave)
        tapis.rename(
            file_path,
            destination_path,
            system_id=system_id,
            force=force_action,
            agave=agave)
        listing = agave.files.list(
            filePath=os.path.dirname(file_path), systemId=system_id)
        files = [tapis.utils.normpath(f.get('path')) for f in listing]
        assert tapis.utils.normpath(destination_path) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()


@pytest.mark.parametrize(
    "src_file_path, file_path, system_id, destination_path, force_action, test_pass",
    [('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-move.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-moved.rst', True,
      True),
     ('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-move.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-moved.rst', False,
      False),
     ('/sample/tacc-cloud/README.rst', '/sample/tacc-cloud/README-move.rst',
      'data-sd2e-community', '/sample/tacc-cloud/README-moved.rst', True, True)
     ])
def test_tapis_manage_move(agave, src_file_path, file_path, system_id,
                           destination_path, force_action, test_pass):
    """Tapis copy can rename a path on the given storageSystem refusing
    to overwrite unless force=True
    """

    def exceptable_code():
        tapis.copy(
            src_file_path,
            file_path,
            system_id=system_id,
            force=True,
            agave=agave)
        tapis.move(
            file_path,
            destination_path,
            system_id=system_id,
            force=force_action,
            agave=agave)
        listing = agave.files.list(
            filePath=os.path.dirname(file_path), systemId=system_id)
        files = [tapis.utils.normpath(f.get('path')) for f in listing]
        assert tapis.utils.normpath(destination_path) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()


@pytest.mark.parametrize(
    "file_path, system_id",
    [('/sample/tacc-cloud/test-mkdir', 'data-sd2e-community'),
     ('/sample/tacc-cloud/test-mkdir-1', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-copy.rst', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-move.rst', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-moved.rst', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-copy-1.rst', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-copy-2.rst', 'data-sd2e-community'),
     ('/sample/tacc-cloud/README-copy-3.rst', 'data-sd2e-community')])
def test_tapis_manage_delete(agave, file_path, system_id):
    """Tapis delete can delete files and directories. In addition to
    being a unit test, this also cleans up artifacts from the mkdir,
    copy, rename, and move tests
    """
    tapis.delete(file_path, system_id=system_id, permissive=True, agave=agave)
