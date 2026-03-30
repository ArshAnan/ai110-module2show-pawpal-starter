from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=20, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feed", duration_minutes=5, priority="high"))
    assert len(pet.tasks) == 1
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 2


def test_scheduler_skips_tasks_that_dont_fit():
    owner = Owner(name="Jordan", available_minutes=10)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Short task", duration_minutes=5, priority="high"))
    pet.add_task(Task(title="Long task", duration_minutes=60, priority="medium"))
    owner.add_pet(pet)

    plan = Scheduler(owner).generate_plan()
    assert len(plan.scheduled_tasks) == 1
    assert len(plan.skipped_tasks) == 1
    assert plan.skipped_tasks[0].title == "Long task"


def test_scheduler_orders_by_priority():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Luna", species="cat")
    pet.add_task(Task(title="Low task", duration_minutes=5, priority="low"))
    pet.add_task(Task(title="High task", duration_minutes=5, priority="high"))
    pet.add_task(Task(title="Medium task", duration_minutes=5, priority="medium"))
    owner.add_pet(pet)

    plan = Scheduler(owner).generate_plan()
    titles = [t.title for t in plan.scheduled_tasks]
    assert titles == ["High task", "Medium task", "Low task"]
