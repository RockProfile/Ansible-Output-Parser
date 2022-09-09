import pytest

from ansible_parser.tasks import Tasks


@pytest.mark.parametrize(
    "filename,has_failures,task_name",
    [
        (
            "task_with_fatal.txt",
            True,
            "Gathering Facts",
        ),
    ],
)
def test_task_info(filename, has_failures, task_name):
    file_content = ""
    with open(f"test/test_data/playbooks/{filename}", "r") as handler:
        file_content = handler.read()
    task = Tasks(file_content)

    assert task.has_failures == has_failures


@pytest.mark.parametrize(
    "filename,expected_all,expected_failures",
    [
        (
            'task_with_fatal.txt',
            8,
            1,
        ),
    ],
)
def test_task_results_count(filename, expected_all, expected_failures):
    file_content = ''
    with open(f'test/test_data/playbooks/{filename}', 'r') as handler:
        file_content = handler.read()
    task = Tasks(file_content)

    assert len(task.results) == expected_all
    assert len(task.failures) == expected_failures
