#testing grounds to make sure logic works before adding UI and backend

from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner
owner = Owner("Alex")

# Create pets
dog = Pet("Buddy", "Dog", 3)
cat = Pet("Luna", "Cat", 5)

# Add tasks to Buddy
dog.add_task(Task("Morning walk", "7:00 AM", "daily"))
dog.add_task(Task("Feeding", "12:00 PM", "daily"))

# Add tasks to Luna
cat.add_task(Task("Evening feeding", "6:00 PM", "daily"))
cat.add_task(Task("Vet checkup", "10:00 AM", "monthly"))

# Link pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Set up scheduler
scheduler = Scheduler()
scheduler.add_owner(owner)

# Print Today's Schedule
print("===== Today's Schedule =====")
for owner_name, pet_name, task in scheduler.get_pending_tasks():
    print(f"[{task.time}] {pet_name} ({owner_name}): {task.description} [{task.frequency}]")
