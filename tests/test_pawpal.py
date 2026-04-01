from pawpal_system import Task, Pet

def test_mark_complete_changes_status():
    task = Task("Morning walk", "7:00 AM", "daily")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True

def test_add_task_increases_pet_task_count():
    pet = Pet("Buddy", "Dog", 3)
    assert len(pet.tasks) == 0
    pet.add_task(Task("Feeding", "12:00 PM", "daily"))
    assert len(pet.tasks) == 1
