from dataclasses import dataclass

@dataclass
class Task:
    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self):
        self.completed = True

    def __repr__(self):
        status = "Done" if self.completed else "Pending"
        return f"Task('{self.description}', time='{self.time}', frequency='{self.frequency}', status={status})"


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

    def get_tasks_by_frequency(self, frequency: str) -> list[tuple[str, str, Task]]:
        """Return all tasks matching the given frequency (e.g. 'daily', 'weekly')."""
        return [(owner, pet, task) for owner, pet, task in self.get_all_tasks()
                if task.frequency.lower() == frequency.lower()]

    def summary(self) -> None:
        """Print a summary of all tasks grouped by owner and pet."""
        for owner in self.owners:
            print(f"Owner: {owner.name}")
            for pet in owner.pets:
                print(f"  Pet: {pet.name} ({pet.species})")
                for task in pet.tasks:
                    print(f"    - {task}")
