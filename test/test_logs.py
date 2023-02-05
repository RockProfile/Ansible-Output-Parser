"""Collection of tests for Logs."""
from datetime import datetime

import pytest

from ansible_parser.logs import Logs


@pytest.mark.parametrize(
    "filename,start_from,expected_play_count,expected_last_play",
    [
        (
            "test/test_data/logs/ansible.txt",
            None,
            9,
            datetime.strptime('2023-02-05 02:00:03,179', '%Y-%m-%d %H:%M:%S,%f'),
        ),
        (
            "test/test_data/logs/ansible.txt",
            datetime.strptime('2023-02-05 02:00:03', '%Y-%m-%d %H:%M:%S'),
            1,
            datetime.strptime('2023-02-05 02:00:03,179', '%Y-%m-%d %H:%M:%S,%f'),
        ),
        (
            "test/test_data/logs/ansible.txt",
            datetime.strptime('2023-02-05 02:00:04', '%Y-%m-%d %H:%M:%S'),
            0,
            None,
        ),
        (
            "test/test_data/logs/ansible_empty.txt",
            None,
            0,
            None,
        ),
    ],
)
def test_logs(filename, start_from, expected_play_count, expected_last_play):
    """
    Test to ensure logs are parsed properly.

    :param filename: Path to log file to process
    :param start_from: datetime to fetch plays from
    :param expected_play_count: The number of plays expected
    :param last_play_processed: The datetime expected to be the last record
    """
    log_plays = Logs(log_file=filename, from_date=start_from)

    assert len(log_plays.plays) == expected_play_count
    assert log_plays.last_processed_time == expected_last_play
