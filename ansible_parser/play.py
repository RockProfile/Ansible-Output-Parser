import re

from typing import Dict

from ansible_parser.task import Tasks


class Play:
    __slots__ = ['_plays', '_current_play']

    def __init__(self, play_output: str):
        self._plays: Dict[str, Dict[str, Tasks]] = {}
        self._process_play(play_output)

    def _process_play(self, play_output: str):
        items = play_output.split('\n\n')
        for item in items:
            item = item.strip()
            if item.startswith('PLAY RECAP'):
                self._process_play_recap(item)
                continue
            if item.startswith('PLAY'):
                self._process_play_info(item)
                continue
            if item.startswith('TASK'):
                tasks: Tasks = Tasks(item)
                self._plays[self._current_play][tasks.name] = tasks
                continue

    def _process_play_info(self, play_output: str):
        self._current_play = re.findall(r'(?:play(?: )+\[)(.+)(?:](?:[ *]+))', play_output, re.IGNORECASE)[0]
        self._plays[self._current_play] = {}

    def _process_play_recap(self, play_output: str):
        pass


with open('../test/example_output/simple.txt') as fh:
    b = Play(fh.read())
print(b)
