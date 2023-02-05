"""Module for parsing play information."""
import re
from typing import Dict, List

from ansible_parser.tasks import Tasks


class Play:
    """Class to handle parsing play information."""

    __slots__ = ["_plays", "_current_play", "_recap", "_warnings"]

    def __init__(self, play_output: str):
        """
        Init that will start the process of analysing the Ansible results.

        Args:
             play_output: The output from Ansible after running commands.
        """
        self._warnings: List[str] = []
        self._plays: Dict[str, Dict[str, Tasks]] = {}
        self._process_warnings(play_output)
        self._process_play(play_output)

    def _process_warnings(self, play_output: str):
        """
        Process any warnings showing in the output.

        :param play_output: Output from running a play
        """
        self._warnings = re.findall(r"\[WARNING]: (.+)", play_output, re.IGNORECASE)

    def _process_play(self, play_output: str):
        """
        Process each section of the play.

        :param play_output: Output of the play.
        """
        items = play_output.split("\n\n")
        for item in items:
            item = item.strip()
            if item.startswith("PLAY RECAP *"):
                self._process_play_recap(item)
                continue
            if item.startswith("PLAY ["):
                self._process_play_info(item)
                continue
            if item.startswith("TASK ["):
                tasks: Tasks = Tasks(item)
                self._plays[self._current_play][tasks.name] = tasks
                continue

    def _process_play_info(self, play_output: str):
        """
        Obtain the name of the current play.

        :param play_output: Play detail line.
        """
        self._current_play = re.findall(
            r"(?:play(?: )+\[)(.+)(?:](?:[ *]+))", play_output, re.IGNORECASE
        )[0]
        self._plays[self._current_play] = {}

    def _process_play_recap(self, play_recap_output: str):
        """
        Parse and stores the recap of the provided play. Only the last play recap is retained.

        :param play_recap_output: The play recap text block.
        """
        self._recap = {}
        recap_items = play_recap_output.split("\n")
        for recap_item in recap_items[1:]:
            recap_details = {}
            recap_item_split = re.findall(
                r"(.+): ([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+(?: )+)"
                r"([a-z]+=[0-9]+)",
                recap_item,
                re.IGNORECASE,
            )
            host = recap_item_split[0][0].strip()
            for recap_status in recap_item_split[0][1:]:
                recap_status = recap_status.strip()
                recap_status_split = recap_status.split("=")
                recap_details[recap_status_split[0]] = int(recap_status_split[1])
            self._recap[host] = recap_details

    def failures(self) -> Dict[str, Dict[str, Dict[str, List[Dict[str, str]]]]]:
        """
        Fetch all failures for the plays.

        :return: Dictionary containing failures.
        """
        failures = {}
        for play in self._plays.keys():
            for task in self._plays[play].keys():
                if self._plays[play][task].has_failures:
                    failures[play] = self._plays[play][task].failures
        return failures

    def plays(self) -> Dict[str, Dict[str, Tasks]]:
        """
        Fetch all plays.

        :return: Dictionary containing plays.
        """
        return self._plays
