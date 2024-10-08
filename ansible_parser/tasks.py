"""Module for parsing task information."""
import itertools
import re
from typing import Dict, List

OK_STATUS_LIST = ["changed", "ok", "skipping"]


class Tasks:
    """Class to handle parsing task information."""

    __slots__ = ["_name", "_task_list"]

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
        tasks_split = tasks_info.split("\n")
        try:
            self._name = re.findall(
                r"(?:TASK(?: )+\[)(.+)(?:](?:[ *]+))", tasks_split[0], re.IGNORECASE
            )[0]
        except KeyError:
            self._name = "Unnamed"

        async_data_items: Dict[str, List[Dict[str, str]]] = {}
        for task_info in tasks_split[1:]:
            if task_info.lower().startswith("async"):
                async_data = re.match(
                    (
                        r"async (?P<status>[a-z0-9)]+) on (?P<hostname>[^:]+): jid=(?P<jid>[0-9.]+)"
                        + r"(?: started=(?P<started>[0-9]))?(?: finished=(?P<finished>[0-9]))?"
                    ),
                    task_info,
                    re.IGNORECASE
                )
                if not async_data:
                    continue
                if async_data.group("jid") not in async_data_items:
                    async_data_items[async_data.group("jid")] = []
                async_data_item = {
                    "status": async_data.group("status"),
                    "hostname": async_data.group("hostname"),
                    "started": async_data.group("started"),
                    "finished": async_data.group("finished"),
                }
                async_data_items[async_data.group("jid")].append(async_data_item)
                continue
            task_details = re.findall(
                (
                    r"(?P<status>[a-z]+):[ ]+\[(?P<hostname>[^\]]+)]"
                    + r"(?:(?:.)+\"ansible_job_id\": \"(?P<job_id>[0-9.]+)\")?(?::[ ]+(.+))?"
                ),
                task_info,
                re.IGNORECASE,
            )
            if not task_details:
                print(f"WARNING: Failed parsing line '{task_info}'")
                continue
            task = {
                "host": task_details[0][1],
                "status": task_details[0][0].lower(),
                "job_id": task_details[0][2] or None,
                "async_info": async_data_items.get(task_details[0][2]),
            }
            task["failure_message"] = task_details[0][3] or None
            if task["status"] not in self._task_list.keys():
                self._task_list[task["status"]] = []
            self._task_list[task["status"]].append(task)

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
        Check to see if any jobs failed.

        :return: True f failed job identified.
        """
        return any(
            task_result_status not in OK_STATUS_LIST
            for task_result_status in self._task_list.keys()
        )

    @property
    def failures(self) -> Dict[str, Dict[str, List[Dict[str, str]]]]:
        """
        Fetch the tasks that failed.

        :return: Failed tasks identified.
        """
        result = {self.name: self._task_list.copy()}
        for task_result_status in self._task_list.keys():
            if task_result_status in OK_STATUS_LIST:
                del result[self.name][task_result_status]
        return result

    @property
    def results(self) -> List[Dict[str, str]]:
        """
        Fetch all the tasks.

        :return: Tasks.
        """
        return list(itertools.chain(*self._task_list.values()))
