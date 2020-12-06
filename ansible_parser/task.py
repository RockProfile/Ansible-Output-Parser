import re

from typing import Dict, List, NoReturn


class Tasks:
    __slots__ = ['_name', '_task_list']

    def __init__(self, tasks_info: str):
        self._task_list: Dict[str, List[Dict[str, str]]] = {}
        self._process_tasks(tasks_info)

    def _process_tasks(self, tasks_info: str):
        tasks_split = tasks_info.split('\n')
        try:
            self._name = re.findall(r'(?:TASK(?: )+\[)(.+)(?:](?:[ *]+))', tasks_split[0], re.IGNORECASE)[0]
        except KeyError:
            self._name = 'Unnamed'
        for task_info in tasks_split[1:]:
            task = {}
            task_details = re.findall(r'([a-z]+):[ ]+\[(.+)](?::[ ]+(.+))?', task_info, re.IGNORECASE)
            task['host'] = task_details[0][1]
            task['status'] = task_details[0][0]
            task['failure_message'] = task_details[0][2]
            if task['status'] not in self._task_list.keys():
                self._task_list[task['status']] = list()
            self._task_list[task['status']].append(task)

    @property
    def name(self) -> str:
        return self._name
