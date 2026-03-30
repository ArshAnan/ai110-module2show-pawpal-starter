from datetime import date, timedelta
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


def test_sort_by_time_orders_correctly():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Late task", duration_minutes=10, priority="low", start_time="11:00"))
    pet.add_task(Task(title="Early task", duration_minutes=10, priority="low", start_time="07:30"))
    pet.add_task(Task(title="No time task", duration_minutes=10, priority="low"))
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())
    assert sorted_tasks[0].title == "Early task"
    assert sorted_tasks[1].title == "Late task"
    assert sorted_tasks[2].title == "No time task"


def test_filter_tasks_by_pet_name():
    owner = Owner(name="Jordan", available_minutes=60)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(Task(title="Walk", duration_minutes=20, priority="high"))
    luna.add_task(Task(title="Feed", duration_minutes=5, priority="high"))
    owner.add_pet(mochi)
    owner.add_pet(luna)

    results = Scheduler(owner).filter_tasks(pet_name="Mochi")
    assert len(results) == 1
    assert results[0].title == "Walk"


def test_filter_tasks_by_completion():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    done = Task(title="Done task", duration_minutes=5, priority="low", completed=True)
    pending = Task(title="Pending task", duration_minutes=5, priority="high")
    pet.add_task(done)
    pet.add_task(pending)
    owner.add_pet(pet)

    incomplete = Scheduler(owner).filter_tasks(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].title == "Pending task"


def test_recurring_daily_task_spawns_next_occurrence():
    today = date.today()
    task = Task(title="Walk", duration_minutes=20, priority="high", frequency="daily", due_date=today)
    next_task = task.mark_complete()
    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False


def test_once_task_returns_none_on_complete():
    task = Task(title="Bath", duration_minutes=15, priority="medium", frequency="once")
    result = task.mark_complete()
    assert result is None


def test_detect_conflicts_finds_overlap():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", start_time="08:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="high", start_time="08:10"))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]


def test_detect_conflicts_no_overlap():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="high", start_time="08:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="high", start_time="09:00"))
    owner.add_pet(pet)

    warnings = Scheduler(owner).detect_conflicts()
    assert len(warnings) == 0
