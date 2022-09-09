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


@pytest.mark.parametrize(
    "filename",
    [
        'task_with_command.txt',
        'task_with_debug_msg.txt',
        'task_with_debug_var.txt',
    ],
)
def test_skipping_debug(filename):
    with open(f'test/test_data/tasks/{filename}', 'r') as handler:
        file_content = handler.read()
    try:
        play = Tasks(file_content)
    except IndexError as e:
        pytest.fail(f'Failed with IndexError: {e}')
