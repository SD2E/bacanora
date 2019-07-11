import os
import pytest
import warnings

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
DATA_DIR = os.path.join(PARENT, 'tests/data/direct')

from bacanora import direct, runtimes


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # directory exists
        ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
         True),
        # file exists
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-community', True, True),
        # fail because file cannot be found, raise UnknowableOutcome
        ('/tests/data/direct/sample/tacc-cloud/dawnofmeep.jpg',
         'data-sd2e-community', False, False),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-fake-system', False, False)
    ])
def test_direct_stat_exists(project_dir, agave, file_path, system_id, exists,
                            test_pass):
    """Test permutations of direct.stat.exists()
    """

    def exceptable_code():
        try:
            fp_exists = direct.exists(
                file_path,
                system_id=system_id,
                runtime=runtimes.LOCALHOST,
                agave=agave)
            if exists:
                assert fp_exists is exists, 'mismatched exists() result'
        except Exception:
            raise

    if test_pass:
        exceptable_code()
    else:
        if exists:
            with pytest.raises(direct.UnknowableOutcome):
                exceptable_code()
        else:
            with pytest.raises(direct.DirectOperationFailed):
                exceptable_code()


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # path exists but is directory
        ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', False,
         True),
        # path exists and is directory
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-community', True, True),
        # fail because file not found, raise UnknowableOutcome
        ('/tests/data/direct/sample/tacc-cloud/dawnofmeep.jpg',
         'data-sd2e-community', False, False),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-fake-system', False, False)
    ])
def test_direct_stat_isfile(project_dir, agave, file_path, system_id, exists,
                            test_pass):
    """Test permutations of direct.stat.isfile()
    """

    def exceptable_code():
        try:
            fp_exists = direct.exists(
                file_path,
                system_id=system_id,
                runtime=runtimes.LOCALHOST,
                agave=agave)
            if exists:
                assert fp_exists is exists, 'mismatched exists() result'
        except Exception:
            raise

    if test_pass:
        exceptable_code()
    else:
        if exists:
            with pytest.raises(direct.UnknowableOutcome):
                exceptable_code()
        else:
            with pytest.raises(direct.DirectOperationFailed):
                exceptable_code()


@pytest.mark.parametrize(
    "file_path, system_id, exists, test_pass",
    [
        # path exists and is directory
        ('/tests/data/direct/sample/tacc-cloud', 'data-sd2e-community', True,
         True),
        # path exists but is not directory
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-community', False, True),
        # fail because file not found, raise UnknowableOutcome
        ('/tests/data/direct/sample/tacc-cloud/dawnofmeep.jpg',
         'data-sd2e-community', False, False),
        # fail because system is non-existent, raise DirectOperationFailed
        ('/tests/data/direct/sample/tacc-cloud/dawnofman.jpg',
         'data-sd2e-fake-system', False, False)
    ])
def test_direct_stat_isdir(project_dir, agave, file_path, system_id, exists,
                           test_pass):
    """Test permutations of direct.stat.isdir()
    """

    def exceptable_code():
        try:
            fp_exists = direct.exists(
                file_path,
                system_id=system_id,
                runtime=runtimes.LOCALHOST,
                agave=agave)
            if exists:
                assert fp_exists is exists, 'mismatched exists() result'
        except Exception:
            raise

    if test_pass:
        exceptable_code()
    else:
        if exists:
            with pytest.raises(direct.UnknowableOutcome):
                exceptable_code()
        else:
            with pytest.raises(direct.DirectOperationFailed):
                exceptable_code()
