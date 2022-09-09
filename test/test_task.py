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
    assert task._name == task_name
