#testing grounds to make sure logic works before adding UI and backend

from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner
owner = Owner("Alex")

# Create pets
dog = Pet("Buddy", "Dog", 3)
cat = Pet("Luna", "Cat", 5)

# --- Fixed tasks (anchored to a specific time) ---
dog.add_task(Task("Morning walk",  duration=30, priority="high",   frequency="daily",  start_time="08:00 AM"))
cat.add_task(Task("Vet checkup",   duration=60, priority="high",   frequency="once",   start_time="10:00 AM"))
# This grooming overlaps with the vet checkup (10:00–11:00 AM) — should trigger a conflict
dog.add_task(Task("Grooming",      duration=45, priority="medium", frequency="once",   start_time="10:30 AM"))

# --- Floating tasks (no start time — scheduler will place these) ---
dog.add_task(Task("Feeding",       duration=10, priority="high",   frequency="daily"))
cat.add_task(Task("Evening feeding", duration=10, priority="high", frequency="daily"))
dog.add_task(Task("Brush teeth",   duration=5,  priority="medium", frequency="weekly"))
cat.add_task(Task("Playtime",      duration=20, priority="low",    frequency="daily"))

# Link pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Set up scheduler
scheduler = Scheduler()
scheduler.add_owner(owner)

# --- Test: mark a daily task complete and check recurrence ---
print("===== Testing mark_complete() recurrence =====")
walk_task = dog.tasks[0]
new_task = walk_task.mark_complete()
if new_task:
    dog.add_task(new_task)
    print(f"'{walk_task.description}' marked done. New occurrence created: {new_task}")
else:
    print(f"'{walk_task.description}' marked done. No recurrence.")

# --- Test: detect_conflicts() ---
print("\n===== Conflict Detection =====")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"WARNING: {warning}")
else:
    print("No conflicts detected.")

# --- Print Today's Schedule sorted by priority ---
print("\n===== Today's Schedule (by priority) =====")
priority_order = {"high": 0, "medium": 1, "low": 2}
pending = scheduler.get_pending_tasks()
pending.sort(key=lambda x: priority_order.get(x[2].priority, 1))
for owner_name, pet_name, task in pending:
    time_label = f"@ {task.start_time}" if task.start_time else "(floating)"
    print(f"[{task.priority:<6}] {pet_name}: {task.description} | {task.duration} min {time_label}")
