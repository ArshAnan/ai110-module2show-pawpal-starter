from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_minutes=60)

mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Tasks with start_times added out of order to demo sorting
mochi.add_task(Task(title="Brush fur",      duration_minutes=10, priority="low",    start_time="09:30", frequency="daily",  due_date=date.today()))
mochi.add_task(Task(title="Morning walk",   duration_minutes=20, priority="high",   start_time="08:00", frequency="daily",  due_date=date.today()))

luna.add_task(Task(title="Play session",    duration_minutes=15, priority="medium", start_time="10:00"))
luna.add_task(Task(title="Give medication", duration_minutes=5,  priority="high",   start_time="08:10"))  # overlaps with Morning walk window
luna.add_task(Task(title="Clean litter box",duration_minutes=10, priority="medium", start_time="11:00"))

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)

# --- 1. Generate priority-based plan ---
print("\n--- Priority-Based Plan ---")
plan = scheduler.generate_plan()
plan.display()

# --- 2. Sort all tasks by start_time ---
print("\n--- All Tasks Sorted by Start Time ---")
all_tasks = owner.get_all_tasks()
for t in scheduler.sort_by_time(all_tasks):
    time_label = t.start_time or "no time"
    print(f"  {time_label}  {t.title} ({t.duration_minutes} min, {t.priority})")

# --- 3. Filter: only Mochi's tasks ---
print("\n--- Mochi's Tasks Only ---")
for t in scheduler.filter_tasks(pet_name="Mochi"):
    print(f"  {t.title} — completed: {t.completed}")

# --- 4. Recurring task: mark Mochi's walk complete, get tomorrow's instance ---
print("\n--- Recurring Task Demo ---")
walk = mochi.tasks[1]  # Morning walk
next_walk = walk.mark_complete()
print(f"  Marked '{walk.title}' complete for {walk.due_date}")
if next_walk:
    print(f"  Next occurrence: '{next_walk.title}' on {next_walk.due_date}")

# --- 5. Filter: only incomplete tasks ---
print("\n--- Incomplete Tasks Only ---")
for t in scheduler.filter_tasks(completed=False):
    print(f"  {t.title}")

# --- 6. Conflict detection ---
print("\n--- Conflict Detection ---")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  ⚠️  {warning}")
else:
    print("  No conflicts detected.")
