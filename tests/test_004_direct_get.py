import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')
TMP_DIR = os.path.join(CWD, 'tmp')

from bacanora import direct, runtimes, settings


@pytest.mark.parametrize(
    "file_path, system_id, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', True)])
def test_direct_get_cwd(project_dir, agave, file_path, system_id, test_pass):
    local_fname = os.path.basename(file_path)

    def exceptable_code():
        direct.get(
            file_path,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            agave=agave)
        files = os.listdir('.')
        assert local_fname in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'tmp/ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'dawnofman.jpg', True)])
def test_direct_get_named(project_dir, agave, file_path, system_id,
                          local_filename, test_pass):
    """Download operation functions in a localhost runtime
    """
    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'

    def exceptable_code():
        direct.get(
            file_path,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            local_filename=local_filename,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, test_pass",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'tmp/ape.jpg', True),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'dawnofman.jpg', True)])
def test_direct_get_no_atomic(project_dir, agave, file_path, system_id,
                              local_filename, test_pass):
    """Download operation functions in a localhost runtime without
    atomic operation support
    """
    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'

    def exceptable_code():
        direct.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            runtime=runtimes.LOCALHOST,
            force=True,
            atomic=False,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()

    try:
        os.unlink(local_fname)
    except SystemError:
        warnings.warn('Failed to unlink {}'.format(local_fname))


@pytest.mark.parametrize(
    "file_path, system_id, local_filename, force_action, test_pass, is_final",
    [('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape-force-1.jpg', True, True, False),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-sd2e-community', 'ape-force-1.jpg', False, False, False),
     ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
      'data-projects-safegenes', 'ape-force-1.jpg', True, True, True)])
def test_direct_get_force(project_dir, agave, file_path, system_id,
                          local_filename, force_action, test_pass, is_final):
    """Download will not overwrite existing file without force=True
    """
    local_fname = local_filename
    local_dest_dir = os.path.dirname(local_fname)
    if local_dest_dir == '':
        local_dest_dir = '.'

    def exceptable_code():

        direct.get(
            file_path,
            system_id=system_id,
            local_filename=local_filename,
            force=force_action,
            runtime=runtimes.LOCALHOST,
            atomic=False,
            agave=agave)
        files = os.listdir(local_dest_dir)
        assert os.path.basename(local_fname) in files

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(Exception):
            exceptable_code()

    if is_final:
        try:
            os.unlink(local_fname)
        except SystemError:
            warnings.warn('Failed to unlink {}'.format(local_fname))
