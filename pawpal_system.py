from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Task:
    description: str
    duration: int              # in minutes
    priority: str              # "low", "medium", or "high"
    frequency: str = "once"    # "once", "daily", or "weekly"
    start_time: str = ""       # optional scheduled start, e.g. "9:00 AM"
    completed: bool = False

    def mark_complete(self):
        """Mark this task complete. Returns a new Task for the next occurrence if recurring."""
        self.completed = True
        if self.frequency in ("daily", "weekly"):
            return Task(self.description, self.duration, self.priority, self.frequency, self.start_time)
        return None

    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return f"Task('{self.description}', duration={self.duration}min, priority='{self.priority}', frequency='{self.frequency}', status={status})"


class Pet:
    def __init__(self, name: str, species: str, age: int) -> None:
        self.name = name
        self.species = species
        self.age = age
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_pending_tasks(self) -> list[Task]:
        return [t for t in self.tasks if not t.completed]

    def __repr__(self):
        return f"Pet(name='{self.name}', species='{self.species}', age={self.age}, tasks={len(self.tasks)})"


class Owner:
    def __init__(self, name: str) -> None:
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[str, Task]]:
        """Return all tasks across all pets as (pet_name, task) pairs."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet.name, task))
        return all_tasks

    def __repr__(self):
        return f"Owner(name='{self.name}', pets={[p.name for p in self.pets]})"


class Scheduler:
    def __init__(self) -> None:
        self.owners: list[Owner] = []

    def add_owner(self, owner: Owner) -> None:
        self.owners.append(owner)

    def get_all_tasks(self) -> list[tuple[str, str, Task]]:
        """Return all tasks as (owner_name, pet_name, task) tuples."""
        result = []
        for owner in self.owners:
            for pet_name, task in owner.get_all_tasks():
                result.append((owner.name, pet_name, task))
        return result

    def get_pending_tasks(self) -> list[tuple[str, str, Task]]:
        """Return only incomplete tasks across all owners and pets."""
        return [(owner, pet, task) for owner, pet, task in self.get_all_tasks() if not task.completed]

    def detect_conflicts(self) -> list[str]:
        """Return warnings for any two fixed tasks whose windows overlap.
        Since one owner handles all pets, overlapping tasks across any pets count as conflicts."""
        fmt = "%I:%M %p"
        fixed = [
            (owner_name, pet_name, task)
            for owner_name, pet_name, task in self.get_all_tasks()
            if task.start_time and not task.completed
        ]
        warnings = []
        for i, (owner_a, pet_a, task_a) in enumerate(fixed):
            start_a = datetime.strptime(task_a.start_time, fmt)
            end_a = start_a + timedelta(minutes=task_a.duration)
            for owner_b, pet_b, task_b in fixed[i + 1:]:
                start_b = datetime.strptime(task_b.start_time, fmt)
                end_b = start_b + timedelta(minutes=task_b.duration)
                if start_a < end_b and end_a > start_b:
                    same_pet = pet_a == pet_b
                    reason = "same pet" if same_pet else f"{owner_a} can't do both at once"
                    warnings.append(
                        f"Conflict ({reason}): '{task_a.description}' ({pet_a}) "
                        f"{task_a.start_time}–{end_a.strftime(fmt)} overlaps "
                        f"'{task_b.description}' ({pet_b}) "
                        f"{task_b.start_time}–{end_b.strftime(fmt)}."
                    )
        return warnings

    def sort_by_duration(self) -> list[tuple[str, str, Task]]:
        """Return all tasks sorted by duration (shortest first)."""
        return sorted(self.get_all_tasks(), key=lambda x: x[2].duration)

    def summary(self) -> None:
        """Print a summary of all tasks grouped by owner and pet."""
        for owner in self.owners:
            print(f"Owner: {owner.name}")
            for pet in owner.pets:
                print(f"  Pet: {pet.name} ({pet.species})")
                for task in pet.tasks:
                    print(f"    - {task}")
