from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"

    def is_feasible(self, remaining_minutes: int) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    owner: Optional["Owner"] = None

    def get_tasks(self) -> list["Task"]:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int):
        self.name = name
        self.available_minutes = available_minutes
        self.pet: Optional[Pet] = None
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_title: str) -> None:
        pass


class Scheduler:
    def __init__(self, owner: Owner, tasks: list[Task]):
        self.owner = owner
        self.tasks = tasks

    def generate_plan(self) -> "Plan":
        pass


class Plan:
    def __init__(
        self,
        scheduled_tasks: list[Task],
        skipped_tasks: list[Task],
        total_duration: int,
    ):
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_duration = total_duration

    def explain(self) -> str:
        pass

    def display(self) -> None:
        pass
