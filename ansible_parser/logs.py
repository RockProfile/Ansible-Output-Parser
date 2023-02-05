"""Module to handle parsing Ansible log files."""
from datetime import datetime
from typing import List, Optional

from ansible_parser.play import Play


class Logs(object):
    """Class to handle parsing Ansible log files."""

    __slots__ = (
        '_from_date',
        '_last_play_time',
        '_plays',
    )

    def __init__(self, log_file: str, from_date: Optional[datetime] = None):
        """
        Init for Logs.

        :param log_file: Full path to the log file
        :param from_date: datetime start extracting plays from
        """
        self._from_date: Optional[datetime] = from_date
        self._last_play_time: Optional[datetime] = None
        self._plays: List[Play] = []
        self._process_log(log_file=log_file)

    def _process_log(self, log_file: str):
        """
        Process the provided log file.

        :param log_file: Full path to the log file
        """
        with open(log_file, 'r') as fh:
            current_play_data = ''
            capture = False
            for line in fh:
                line_part = line.split(' | ')
                if line_part[1].startswith('PLAY ['):
                    date_raw = ' '.join(line_part[0].split(' ')[0:2])
                    if not self.date_of_interest(date=date_raw):
                        capture = False
                        current_play_data = ''
                        continue
                    if current_play_data:
                        self._plays.append(Play(current_play_data))
                        current_play_data = ''
                    current_play_data += line_part[1]
                    capture = True
                elif capture:
                    if line_part[1].startswith('TASK [')\
                            or line_part[1].startswith('PLAY RECAP *')\
                            or line_part[1].startswith('ERROR!'):
                        current_play_data += '\n'
                    current_play_data += line_part[1]
            if current_play_data:
                self._plays.append(Play(current_play_data))

    def date_of_interest(self, date: str) -> bool:
        """
        Check to ensure the date provided is greater than the date of the play.

        :param date: Date the play was carried out

        :return: True if of interest otherwise False
        """
        play_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S,%f')
        if not self._from_date or play_date > self._from_date:
            self._last_play_time = play_date
            return True
        return False

    @property
    def plays(self) -> List[Play]:
        """
        Property to provide found plays.

        :return: List of plays
        """
        return self._plays

    @property
    def last_processed_time(self) -> Optional[datetime]:
        """
        Property to provide the time and date the last play was processed from the log file.

        :return: datetime of the last play or None if no plays processed
        """
        return self._last_play_time
