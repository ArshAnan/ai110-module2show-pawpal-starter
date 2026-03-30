from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _time_to_minutes(t: str) -> int:
    """Convert a 'HH:MM' string to total minutes since midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


@dataclass
class Task:
    """Represents a single pet care activity."""

    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completed: bool = False
    start_time: Optional[str] = None  # "HH:MM" format
    frequency: str = "once"  # "once", "daily", "weekly"
    due_date: Optional[date] = None

    def is_feasible(self, remaining_minutes: int) -> bool:
        """Return True if this task fits within the remaining available time."""
        return self.duration_minutes <= remaining_minutes

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next occurrence if recurring, else None."""
        self.completed = True
        if self.frequency == "daily" and self.due_date:
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(days=1),
                start_time=self.start_time,
            )
        if self.frequency == "weekly" and self.due_date:
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=self.due_date + timedelta(weeks=1),
                start_time=self.start_time,
            )
        return None


@dataclass
class Pet:
    """Stores pet details and a list of care tasks."""

    name: str
    species: str  # "dog", "cat", "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title from this pet's task list."""
        self.tasks = [t for t in self.tasks if t.title != task_title]


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str, available_minutes: int):
        """Initialize an owner with a name and daily time budget in minutes."""
        self.name = name
        self.available_minutes = available_minutes
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """Retrieves, organizes, and generates a daily care plan from an owner's pets."""

    def __init__(self, owner: Owner):
        """Initialize the scheduler with an owner whose pets and tasks will be scheduled."""
        self.owner = owner

    def generate_plan(self) -> "Plan":
        """Sort tasks by priority and fit them within the owner's available time."""
        all_tasks = self.owner.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, 99))

        scheduled = []
        skipped = []
        remaining = self.owner.available_minutes

        for task in sorted_tasks:
            if task.is_feasible(remaining):
                scheduled.append(task)
                remaining -= task.duration_minutes
            else:
                skipped.append(task)

        total_duration = self.owner.available_minutes - remaining
        return Plan(scheduled, skipped, total_duration)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by start_time (HH:MM). Tasks without a start_time sort last."""
        return sorted(tasks, key=lambda t: t.start_time or "99:99")

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
    ) -> list[Task]:
        """Filter tasks by pet name and/or completion status. Omit a parameter to skip that filter."""
        results = []
        for pet in self.owner.pets:
            if pet_name and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if completed is not None and task.completed != completed:
                    continue
                results.append(task)
        return results

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any tasks whose time windows overlap."""
        timed_tasks = [t for t in self.owner.get_all_tasks() if t.start_time]
        warnings = []
        for i, a in enumerate(timed_tasks):
            for b in timed_tasks[i + 1:]:
                a_start = _time_to_minutes(a.start_time)
                a_end = a_start + a.duration_minutes
                b_start = _time_to_minutes(b.start_time)
                b_end = b_start + b.duration_minutes
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"CONFLICT: '{a.title}' ({a.start_time}, {a.duration_minutes} min) "
                        f"overlaps with '{b.title}' ({b.start_time}, {b.duration_minutes} min)"
                    )
        return warnings


class Plan:
    """Holds the result of a scheduling run: what was scheduled, what was skipped, and why."""

    def __init__(
        self,
        scheduled_tasks: list[Task],
        skipped_tasks: list[Task],
        total_duration: int,
    ):
        """Initialize a plan with scheduled tasks, skipped tasks, and total time used."""
        self.scheduled_tasks = scheduled_tasks
        self.skipped_tasks = skipped_tasks
        self.total_duration = total_duration

    def explain(self) -> str:
        """Return a human-readable explanation of why each task was scheduled or skipped."""
        lines = []
        for task in self.scheduled_tasks:
            lines.append(
                f"  [SCHEDULED] {task.title} ({task.duration_minutes} min, {task.priority} priority)"
            )
        for task in self.skipped_tasks:
            lines.append(
                f"  [SKIPPED]   {task.title} ({task.duration_minutes} min) — not enough time remaining"
            )
        return "\n".join(lines)

    def display(self) -> None:
        """Print the full plan to the terminal."""
        print("=" * 40)
        print("        TODAY'S PAW PLAN")
        print("=" * 40)
        print(self.explain())
        print("-" * 40)
        print(f"  Total time used: {self.total_duration} min")
        print("=" * 40)
