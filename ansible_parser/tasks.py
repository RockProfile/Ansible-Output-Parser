import re

from typing import Dict, List

OK_STATUS_LIST = ['changed', 'ok', 'skipping']


class Tasks:
    __slots__ = ['_name', '_task_list']

    def __init__(self, tasks_info: str):
        """
        Init that starts the process of analysing a task.

        :param tasks_info: Task block from Ansible output.
        """
        self._task_list: Dict[str, List[Dict[str, str]]] = {}
        self._process_tasks(tasks_info)

    def _process_tasks(self, tasks_info: str):
        """
        Process task and store the result.

        :param tasks_info: Task block to be analysed.
        """
        tasks_split = tasks_info.split('\n')
        try:
            self._name = re.findall(r'(?:TASK(?: )+\[)(.+)(?:](?:[ *]+))', tasks_split[0], re.IGNORECASE)[0]
        except KeyError:
            self._name = 'Unnamed'
        for task_info in tasks_split[1:]:
            task = {}
            task_details = re.findall(r'([a-z]+):[ ]+\[(.+)](?::[ ]+(.+))?', task_info, re.IGNORECASE)
            task['host'] = task_details[0][1]
            task['status'] = task_details[0][0].lower()
            task['failure_message'] = task_details[0][2]
            if task['status'] not in self._task_list.keys():
                self._task_list[task['status']] = list()
            self._task_list[task['status']].append(task)

    @property
    def name(self) -> str:
        """
        Name of the task.

        :return: Task name.
        """
        return self._name

    @property
    def has_failures(self) -> bool:
        """
        Checks to see if any jobs failed

        :return: True f failed job identified.
        """
        for task_result_status in self._task_list.keys():
            if task_result_status not in OK_STATUS_LIST:
                return True
        return False

    @property
    def failures(self) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        Fetches the tasks that failed.

        :return: Failed tasks identified.
        """
        result = {self.name: self._task_list.copy()}
        for task_result_status in self._task_list.keys():
            if task_result_status in OK_STATUS_LIST:
                del result[self.name][task_result_status]
        return result
