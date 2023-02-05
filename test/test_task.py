"""Collection of tests for Tasks."""
import pytest

from ansible_parser.tasks import Tasks


@pytest.mark.parametrize(
    "filename,has_failures,task_name",
    [
        (
            "test/test_data/playbooks/task_with_fatal.txt",
            True,
            "Gathering Facts",
        ),
    ],
)
def test_task_info(filename, has_failures, task_name):
    """
    Test to ensure task information is correct.

    :param filename: Path to playbook to test
    :param has_failures: True if the playbook has failures
    :param task_name: The expected name of the play
    """
    with open(filename, "r") as handler:
        file_content = handler.read()
    task = Tasks(file_content)

    assert task.has_failures == has_failures


@pytest.mark.parametrize(
    "filename,expected_all,expected_failures",
    [
        (
            'test/test_data/playbooks/task_with_fatal.txt',
            8,
            1,
        ),
    ],
)
def test_task_results_count(filename, expected_all, expected_failures):
    """
    Test to ensure task information is correct.

    :param filename: Path to playbook to test
    :param expected_all: The number of tasks expected
    :param expected_failures: The number of failures expected
    """
    with open(filename, 'r') as handler:
        file_content = handler.read()
    task = Tasks(file_content)

    assert len(task.results) == expected_all
    assert len(task.failures) == expected_failures


@pytest.mark.parametrize(
    "filename",
    [
        'test/test_data/tasks/task_with_command.txt',
        'test/test_data/tasks/task_with_debug_msg.txt',
        'test/test_data/tasks/task_with_debug_var.txt',
    ],
)
def test_skipping_debug(filename):
    """
    Test to ensure debug information is skipped.

    :param filename: Path to playbook to test
    """
    with open(filename, 'r') as handler:
        file_content = handler.read()
    try:
        _ = Tasks(file_content)
    except IndexError as e:
        pytest.fail(f'Failed with IndexError: {e}')
