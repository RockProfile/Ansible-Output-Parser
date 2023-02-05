"""Collection of tests for Plays."""
import pytest

from ansible_parser.play import Play


@pytest.mark.parametrize(
    "filename,expected",
    [
        (
            "failed_with_warning.txt",
            ["Found both group and host with same name: test"],
        ),
        (
            "multiple_devices.txt",
            [],
        ),
        (
            "multiple_playbooks.txt",
            [],
        ),
        (
            "ok_with_warning.txt",
            ["Found both group and host with same name: test"],
        ),
        (
            "simple.txt",
            [],
        ),
    ],
)
def test_warning(filename, expected):
    """Test warnings are captured correctly."""
    with open(f"test/test_data/playbooks/{filename}", "r") as handler:
        file_content = handler.read()
    play = Play(file_content)
    assert play._warnings == expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        (
            'failed_with_warning.txt',
            1,
        ),
        (
            'multiple_devices.txt',
            1,
        ),
        (
            'multiple_playbooks.txt',
            2,
        ),
        (
            'ok_with_warning.txt',
            1,
        ),
        (
            'simple.txt',
            1,
        ),
    ],
)
def test_plays_count(filename, expected):
    """Test to ensure plays result in the correct number of tasks."""
    with open(f'test/test_data/playbooks/{filename}', 'r') as handler:
        file_content = handler.read()
    play = Play(file_content)
    assert len(play.plays()) == expected
