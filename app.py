import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state setup ---
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if st.button("Set Owner"):
    owner = Owner(owner_name)
    st.session_state.owner = owner
    st.session_state.scheduler.add_owner(owner)
    st.success(f"Owner set: {owner_name}")

st.divider()

# --- Add a Pet ---
st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.error("Set an owner first.")
    else:
        pet = Pet(pet_name, species, 0)
        st.session_state.owner.add_pet(pet)
        st.success(f"Added {pet_name} the {species}.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if st.session_state.owner and st.session_state.owner.pets:
    pet_options = {p.name: p for p in st.session_state.owner.pets}
    selected_pet_name = st.selectbox("Assign to pet", list(pet_options.keys()))

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    with col5:
        start_time = st.time_input("Start time", value=None)

    if st.button("Add Task"):
        from datetime import datetime, timedelta
        start_time_str = start_time.strftime("%I:%M %p") if start_time else ""
        conflict = None
        if start_time_str:
            fmt = "%I:%M %p"
            new_start = datetime.strptime(start_time_str, fmt)
            new_end = new_start + timedelta(minutes=int(duration))
            for _, pet_name_existing, existing_task in st.session_state.scheduler.get_all_tasks():
                if not existing_task.start_time or existing_task.completed:
                    continue
                ex_start = datetime.strptime(existing_task.start_time, fmt)
                ex_end = ex_start + timedelta(minutes=existing_task.duration)
                if new_start < ex_end and new_end > ex_start:
                    conflict = (pet_name_existing, existing_task)
                    break
        if conflict:
            pet_name_existing, existing_task = conflict
            st.warning(
                f"Conflict: '{task_title}' ({start_time_str}, {duration} min) overlaps "
                f"'{existing_task.description}' for {pet_name_existing} "
                f"({existing_task.start_time}, {existing_task.duration} min). "
                f"Please choose a different start time."
            )
        else:
            task = Task(task_title, duration=int(duration), priority=priority, frequency=frequency, start_time=start_time_str)
            pet_options[selected_pet_name].add_task(task)
            st.success(f"Task '{task_title}' added to {selected_pet_name}.")
else:
    st.info("Add a pet above before adding tasks.")

st.divider()

# --- Generate Schedule ---
st.subheader("Today's Schedule")

priority_order = {"high": 0, "medium": 1, "low": 2}

if "sort_order" not in st.session_state:
    st.session_state.sort_order = None

col_radio, col_clear = st.columns([4, 1])
with col_radio:
    sort_options = ["Shortest first", "Longest first", "Start time"]
    st.session_state.sort_order = st.radio(
        "Sort by", sort_options,
        index=None if st.session_state.sort_order is None else sort_options.index(st.session_state.sort_order),
        horizontal=True
    )
with col_clear:
    if st.button("Clear"):
        st.session_state.sort_order = None
        st.rerun()

sort_order = st.session_state.sort_order

col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
with col_filter2:
    pet_names = [p.name for p in st.session_state.owner.pets] if st.session_state.owner else []
    pet_filter = st.selectbox("Filter by pet", ["All"] + pet_names)

if st.button("Generate Schedule"):
    all_tasks = st.session_state.scheduler.get_all_tasks()
    if not all_tasks:
        st.info("No tasks found.")
    else:
        # Apply filters
        if status_filter == "Pending":
            all_tasks = [(o, p, t) for o, p, t in all_tasks if not t.completed]
        elif status_filter == "Completed":
            all_tasks = [(o, p, t) for o, p, t in all_tasks if t.completed]

        if pet_filter != "All":
            all_tasks = [(o, p, t) for o, p, t in all_tasks if p == pet_filter]

        if not all_tasks:
            st.info("No tasks match the selected filters.")
        else:
            if sort_order == "Shortest first":
                all_tasks.sort(key=lambda x: x[2].duration)
            elif sort_order == "Longest first":
                all_tasks.sort(key=lambda x: x[2].duration, reverse=True)
            elif sort_order == "Start time":
                from datetime import datetime
                all_tasks.sort(key=lambda x: datetime.strptime(x[2].start_time, "%I:%M %p") if x[2].start_time else datetime.max)
            else:
                all_tasks.sort(key=lambda x: priority_order.get(x[2].priority, 1))

            conflicts = st.session_state.scheduler.detect_conflicts()
            if conflicts:
                for warning in conflicts:
                    st.warning(warning)

            pet_lookup = {p.name: p for p in st.session_state.owner.pets} if st.session_state.owner else {}

            header = st.columns([2, 3, 1, 1, 1, 1, 1])
            for col, label in zip(header, ["Pet", "Task", "Start", "Duration", "Priority", "Status", ""]):
                col.markdown(f"**{label}**")

            for i, (owner_name, pet_name, task) in enumerate(all_tasks):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 3, 1, 1, 1, 1, 1])
                col1.write(pet_name)
                col2.write(task.description)
                col3.write(task.start_time if task.start_time else "—")
                col4.write(f"{task.duration} min")
                col5.write(task.priority)
                col6.write("Done" if task.completed else "Pending")
                if not task.completed:
                    if col7.button("Complete", key=f"complete_{i}"):
                        new_task = task.mark_complete()
                        if new_task and pet_name in pet_lookup:
                            pet_lookup[pet_name].add_task(new_task)
                        st.rerun()
