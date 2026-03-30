import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Step 2: Session state "vault" ---
# Streamlit reruns the script on every interaction.
# We store the Owner object in session_state so it persists across reruns.
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Setup ---
st.header("Owner & Time Budget")

with st.form("owner_form"):
    owner_name = st.text_input("Your name", value="Jordan")
    available_minutes = st.number_input(
        "Available time today (minutes)", min_value=5, max_value=480, value=60
    )
    submitted = st.form_submit_button("Save owner")
    if submitted:
        st.session_state.owner = Owner(
            name=owner_name, available_minutes=available_minutes
        )
        st.success(f"Owner '{owner_name}' saved with {available_minutes} min available.")

if st.session_state.owner is None:
    st.info("Set up your owner profile above to get started.")
    st.stop()

owner: Owner = st.session_state.owner

# --- Add a Pet ---
st.divider()
st.header("Pets")

with st.form("pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")
    if add_pet:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)
        st.success(f"Added {species} '{pet_name}'.")

if owner.pets:
    st.write(f"**{owner.name}'s pets:**")
    for pet in owner.pets:
        st.markdown(f"- **{pet.name}** ({pet.species}) — {len(pet.tasks)} task(s)")
else:
    st.info("No pets added yet.")

# --- Add a Task ---
st.divider()
st.header("Tasks")

if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("task_form"):
        pet_names = [p.name for p in owner.pets]
        selected_pet_name = st.selectbox("Assign to pet", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        add_task = st.form_submit_button("Add task")

        if add_task:
            selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)
            selected_pet.add_task(
                Task(title=task_title, duration_minutes=int(duration), priority=priority)
            )
            st.success(f"Added task '{task_title}' to {selected_pet_name}.")

    # Show all tasks across all pets
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("**All current tasks:**")
        rows = [
            {
                "Pet": next(p.name for p in owner.pets if t in p.tasks),
                "Task": t.title,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
            }
            for t in all_tasks
        ]
        st.table(rows)
    else:
        st.info("No tasks yet. Add one above.")

# --- Generate Schedule ---
st.divider()
st.header("Generate Today's Schedule")

if st.button("Generate schedule"):
    all_tasks = owner.get_all_tasks()
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(owner)
        plan = scheduler.generate_plan()

        st.subheader("Scheduled")
        if plan.scheduled_tasks:
            for task in plan.scheduled_tasks:
                st.success(
                    f"**{task.title}** — {task.duration_minutes} min ({task.priority} priority)"
                )
        else:
            st.info("No tasks could be scheduled within your time budget.")

        if plan.skipped_tasks:
            st.subheader("Skipped (not enough time)")
            for task in plan.skipped_tasks:
                st.warning(
                    f"**{task.title}** — {task.duration_minutes} min — not enough time remaining"
                )

        st.metric("Total time used", f"{plan.total_duration} min")
        st.metric("Time budget", f"{owner.available_minutes} min")
