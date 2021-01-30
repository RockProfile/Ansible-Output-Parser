import pytest
from ansible_parser.play import Play


@pytest.mark.parametrize(
    "filename,expected",
    [
        (
            'failed_with_warning.txt',
            ['Found both group and host with same name: test'],
        ),
        (
            'multiple_devices.txt',
            [],
        ),
        (
            'multiple_playbooks.txt',
            [],
        ),
        (
            'ok_with_warning.txt',
            ['Found both group and host with same name: test'],
        ),
        (
            'simple.txt',
            [],
        ),
    ],
)
def test_warning(filename, expected):
    file_content = ''
    with open(f'test/test_data/playbooks/{filename}', 'r') as handler:
        file_content = handler.read()
    play = Play(file_content)
    assert play._warnings == expected
