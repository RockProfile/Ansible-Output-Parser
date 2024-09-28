"""Collection of tests for Plays."""
from typing import List

import pytest

from ansible_parser.play import Play


@pytest.mark.parametrize(
    "filename,expected_warning_list",
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
def test_warning(filename: str, expected_warning_list: List[str]):
    """Test warnings are captured correctly."""
    with open(f"test/test_data/playbooks/{filename}", "r") as handler:
        file_content = handler.read()
    play = Play(file_content)
    assert play._warnings == expected_warning_list


@pytest.mark.parametrize(
    "filename,expected_play_count,expected_failure_count",
    [
        (
            'failed_with_warning.txt',
            1,
            1,
        ),
        (
            "issue-31.txt",
            1,
            1,
        ),
        (
            'multiple_devices.txt',
            1,
            1,  # 1 host unreachable
        ),
        (
            'multiple_playbooks.txt',
            2,
            0,
        ),
        (
            'ok_with_warning.txt',
            1,
            0,
        ),
        (
            'simple.txt',
            1,
            0,
        ),
    ],
)
def test_plays_count(filename: str, expected_play_count: int, expected_failure_count: int):
    """Test to ensure plays result in the correct number of tasks."""
    with open(f'test/test_data/playbooks/{filename}', 'r') as handler:
        file_content = handler.read()
    play = Play(file_content)
    assert len(play.plays()) == expected_play_count, (
        f'{filename} - Play count got {len(play.plays())} expected {expected_failure_count}'
    )
    assert len(play.failures()) == expected_failure_count, (
        f'{filename} - Failure count got {len(play.failures())} expected {expected_failure_count}'
    )
