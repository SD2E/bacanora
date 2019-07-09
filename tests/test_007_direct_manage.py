import os
import pytest
import shutil
import warnings
from .fixtures.agave import agave, credentials

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import direct
from bacanora import utils
from .utils import local_delete


@pytest.mark.parametrize(
    "path_to_make, system_id, root_dir, force_action, test_pass, last_test",
    [('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      True, True, False),
     ('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      False, False, False),
     ('/tests/data/direct/sample/test-mkdir-force', 'data-sd2e-community', '/',
      True, True, True),
     ('test-mkdir-relative', 'data-sd2e-community',
      '/tests/data/direct/sample', True, True, True)])
def test_direct_manage_mkdir(agave, path_to_make, system_id, root_dir,
                             force_action, test_pass, last_test):
    """Ensure mkdir() works for absolute and relative paths, but fails if
    destination exists and force is not True
    """
    final_path_to_make = os.path.join(root_dir, utils.normalize(path_to_make))

    def exceptable_code():
        created_posix_path = direct.abs_path(
            path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)
        direct.mkdir(
            path_to_make,
            system_id=system_id,
            root_dir=root_dir,
            force=force_action,
            agave=agave)
        if force_action:
            assert os.path.exists(
                created_posix_path), '{} did not exist after mkdir()'.format(
                    created_posix_path)
        # direct.exists(
        #     path_to_make, system_id=system_id, root_dir=root_dir, agave=agave)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    if last_test:
        local_delete(final_path_to_make)


@pytest.mark.parametrize(
    "src_path, path_to_copy, system_id, root_dir, force_action, test_pass, last_test",
    [('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-2.png',
      'data-sd2e-community', '/', True, True, False),
     ('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-2.png',
      'data-sd2e-community', '/', False, False, False),
     ('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-2.png',
      'data-sd2e-community', '/', True, True, True),
     ('/tests/data/direct/sample/tacc-cloud',
      '/tests/data/direct/sample/tacc-cloud-copytest', 'data-sd2e-community',
      '/', True, True, True)])
def test_direct_manage_copy(agave, src_path, path_to_copy, system_id, root_dir,
                            force_action, test_pass, last_test):
    """Rename file or directory works but fails if destination exists
    when force is not True
    """

    path_copied_name = path_to_copy + '-copy'

    def exceptable_code():
        # Workalike to avoid testing copy() until we are ready
        src = utils.normalize(src_path)
        dest = utils.normalize(path_to_copy)
        if os.path.isfile(src):
            shutil.copy2(src, dest)
        elif os.path.isdir(src):
            shutil.copytree(src, dest)

        direct.copy(
            path_to_copy,
            path_copied_name,
            system_id=system_id,
            root_dir=root_dir,
            force=force_action,
            agave=agave)
        norm_path_new_name = utils.normalize(path_copied_name)
        assert os.path.exists(norm_path_new_name), '{} was not copied'.format(
            norm_path_new_name)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()

    if last_test:
        for del_target in (path_to_copy, path_copied_name):
            local_delete(del_target)


@pytest.mark.parametrize(
    "src_path, path_to_rename, system_id, root_dir, force_action, test_pass, last_test",
    [('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-1.png',
      'data-sd2e-community', '/', True, True, False),
     ('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-1.png',
      'data-sd2e-community', '/', False, False, False),
     ('/tests/data/direct/sample/tacc-cloud/ansible.png',
      '/tests/data/direct/sample/tacc-cloud/ansible-1.png',
      'data-sd2e-community', '/', True, True, True),
     ('/tests/data/direct/sample/tacc-cloud',
      '/tests/data/direct/sample/tacc-cloud-pytest', 'data-sd2e-community',
      '/', True, True, True)])
def test_direct_manage_rename(agave, src_path, path_to_rename, system_id,
                              root_dir, force_action, test_pass, last_test):
    """Rename file or directory works but fails if destination exists
    when force is not True
    """

    path_new_name = path_to_rename + '-renamed'

    def exceptable_code():
        direct.copy(
            src_path,
            path_to_rename,
            system_id=system_id,
            root_dir=root_dir,
            force=True,
            agave=agave)
        direct.rename(
            path_to_rename,
            path_new_name,
            system_id=system_id,
            root_dir=root_dir,
            force=force_action,
            agave=agave)
        norm_path_new_name = utils.normalize(path_new_name)
        assert os.path.exists(norm_path_new_name), '{} was not copied'.format(
            norm_path_new_name)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()

    if last_test:
        for del_target in (path_to_rename, path_new_name):
            local_delete(del_target)
