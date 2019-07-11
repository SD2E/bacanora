import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')

from bacanora import direct, runtimes


@pytest.mark.parametrize(
    "directory_path, system_id, test_pass",
    [('/tests/data/direct/sample/', 'data-sd2e-community', True),
     ('/tests/data/direct/sample-noexist/', 'data-sd2e-community', False),
     ('/tests/data/direct/sample/tacc-cloud/ansible.png',
      'data-sd2e-community', False),
     ('/tests/data/direct/sample/tacc-cloud', 'data-projects-fake-system',
      False),
     ('/tests/data/direct/sample/tacc-cloud', 'data-projects-safegenes', True)]
)
def test_direct_walk_exceptions(project_dir, agave, directory_path, system_id,
                                test_pass):
    """Exceptions should be raised on various error states
    """

    def exceptable_code():
        resp = direct.walk(
            directory_path,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            agave=agave)
        assert isinstance(resp, list), 'Response was not a list'
        assert len(resp) > 0, 'Response was a list but was empty'

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(direct.DirectOperationFailed):
            exceptable_code()


@pytest.mark.parametrize(
    "directory_path, system_id, directories, diagnostic_value, test_pass",
    [('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
      'nested_directory', True),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', False,
      'nested_directory', False),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', False,
      'no_such_directory', False)])
def test_direct_walk_directories(project_dir, agave, directory_path, system_id,
                                 directories, diagnostic_value, test_pass):
    """Can toggle the return of subdirectories
    """

    def exceptable_code():
        resp = direct.walk(
            directory_path,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            directories=directories,
            agave=agave)
        resp_files = [os.path.basename(f) for f in resp]
        assert diagnostic_value in resp_files, 'Diagnostic value {} was not returned'.format(
            diagnostic_value)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(AssertionError):
            exceptable_code()


@pytest.mark.parametrize(
    "directory_path, system_id, dotfiles, diagnostic_value, test_pass",
    [('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
      '.hidden_file', True),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
      '.nested_hidden_file', True),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', False,
      '.hidden_file', False),
     ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
      '.hidden_file_doesnt_exist', False)])
def test_direct_walk_dotfiles(project_dir, agave, directory_path, system_id,
                              dotfiles, diagnostic_value, test_pass):
    """Can toggle the return of dotfiles in response
    """

    def exceptable_code():
        resp = direct.walk(
            directory_path,
            system_id=system_id,
            runtime=runtimes.LOCALHOST,
            dotfiles=dotfiles,
            agave=agave)
        resp_files = [os.path.basename(f) for f in resp]
        assert diagnostic_value in resp_files, 'Diagnostic value {} was not returned'.format(
            diagnostic_value)

    if test_pass:
        exceptable_code()
    else:
        with pytest.raises(AssertionError):
            exceptable_code()
