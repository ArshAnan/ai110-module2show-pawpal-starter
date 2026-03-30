from pawpal_system import Task, Pet, Owner, Scheduler

# Create owner with 60 minutes available today
owner = Owner(name="Jordan", available_minutes=60)

# Create two pets
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=20, priority="high"))
mochi.add_task(Task(title="Brush fur", duration_minutes=10, priority="low"))

# Add tasks to Luna
luna.add_task(Task(title="Give medication", duration_minutes=5, priority="high"))
luna.add_task(Task(title="Play session", duration_minutes=15, priority="medium"))
luna.add_task(Task(title="Clean litter box", duration_minutes=10, priority="medium"))

# Register pets with owner
owner.add_pet(mochi)
owner.add_pet(luna)

# Generate and display the plan
scheduler = Scheduler(owner)
plan = scheduler.generate_plan()
plan.display()
