from datetime import datetime
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task("Morning walk", duration=30, priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet("Buddy", "Dog", 3)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", duration=10, priority="high"))
    assert len(pet.tasks) == 1


# --- Sorting Correctness ---

def test_sort_by_duration_shortest_first():
    owner = Owner("Alex")
    pet = Pet("Buddy", "Dog", 3)
    pet.add_task(Task("Vet checkup",   duration=60, priority="medium", start_time="10:00 AM"))
    pet.add_task(Task("Feeding",       duration=10, priority="high",   start_time="12:00 PM"))
    pet.add_task(Task("Morning walk",  duration=30, priority="high",   start_time="08:00 AM"))
    owner.add_pet(pet)
    scheduler = Scheduler()
    scheduler.add_owner(owner)

    sorted_tasks = scheduler.sort_by_duration()
    durations = [t[2].duration for t in sorted_tasks]
    assert durations == sorted(durations)


def test_tasks_sorted_by_start_time_chronological():
    tasks = [
        Task("Vet checkup",  duration=60, priority="medium", start_time="10:00 AM"),
        Task("Feeding",      duration=10, priority="high",   start_time="12:00 PM"),
        Task("Morning walk", duration=30, priority="high",   start_time="08:00 AM"),
    ]
    fmt = "%I:%M %p"
    sorted_tasks = sorted(tasks, key=lambda t: datetime.strptime(t.start_time, fmt))
    times = [t.start_time for t in sorted_tasks]
    assert times == ["08:00 AM", "10:00 AM", "12:00 PM"]


# --- Recurrence Logic ---

def test_daily_task_creates_new_task_on_complete():
    task = Task("Morning walk", duration=30, priority="high", frequency="daily")
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.completed == False
    assert new_task.description == "Morning walk"
    assert new_task.frequency == "daily"


def test_once_task_returns_none_on_complete():
    task = Task("Vet checkup", duration=60, priority="high", frequency="once")
    new_task = task.mark_complete()
    assert new_task is None


def test_weekly_task_creates_new_task_on_complete():
    task = Task("Bath time", duration=20, priority="medium", frequency="weekly")
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.frequency == "weekly"


# --- Conflict Detection ---

def test_conflict_detected_for_overlapping_fixed_tasks():
    owner = Owner("Alex")
    dog = Pet("Buddy", "Dog", 3)
    cat = Pet("Luna", "Cat", 5)
    # Walk runs 09:00–10:00, Feeding starts at 09:30 — overlap
    dog.add_task(Task("Walk",    duration=60, priority="high", start_time="09:00 AM"))
    cat.add_task(Task("Feeding", duration=30, priority="high", start_time="09:30 AM"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler()
    scheduler.add_owner(owner)

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Walk" in conflicts[0]
    assert "Feeding" in conflicts[0]


def test_no_conflict_for_non_overlapping_tasks():
    owner = Owner("Alex")
    pet = Pet("Buddy", "Dog", 3)
    # Walk ends at 08:30, Feeding starts at 09:00 — no overlap
    pet.add_task(Task("Morning walk", duration=30, priority="high", start_time="08:00 AM"))
    pet.add_task(Task("Feeding",      duration=10, priority="high", start_time="09:00 AM"))
    owner.add_pet(pet)
    scheduler = Scheduler()
    scheduler.add_owner(owner)

    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0


def test_conflict_includes_owner_name_when_different_pets():
    owner = Owner("Alex")
    dog = Pet("Buddy", "Dog", 3)
    cat = Pet("Luna", "Cat", 5)
    dog.add_task(Task("Walk",        duration=60, priority="high", start_time="09:00 AM"))
    cat.add_task(Task("Vet checkup", duration=30, priority="high", start_time="09:00 AM"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler()
    scheduler.add_owner(owner)

    conflicts = scheduler.detect_conflicts()
    assert any("Alex" in c for c in conflicts)
