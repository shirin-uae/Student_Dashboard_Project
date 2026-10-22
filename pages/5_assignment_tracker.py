import streamlit as st
from datetime import date, timedelta


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Assignment Tracker",
    page_icon="📝",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .page-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .page-subtitle {
        color: #777;
        font-size: 17px;
        margin-top: 4px;
        margin-bottom: 20px;
    }

    .assignment-title {
        font-size: 21px;
        font-weight: 650;
    }

    .muted {
        color: #777;
        font-size: 14px;
    }

    .overdue {
        color: #d32f2f;
        font-weight: 600;
    }

    .due-soon {
        color: #e68a00;
        font-weight: 600;
    }

    .completed {
        color: #2e7d32;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "assignments" not in st.session_state:
    st.session_state.assignments = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "completed_assignments" not in st.session_state:
    st.session_state.completed_assignments = 0

if "activity" not in st.session_state:
    st.session_state.activity = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_status_icon(status):
    if status == "Completed":
        return "✅"
    elif status == "In Progress":
        return "🔄"
    return "⏳"


def get_priority_icon(priority):
    if priority == "High":
        return "🔴"
    elif priority == "Medium":
        return "🟡"
    return "🟢"


def get_due_text(due_date, status):

    if status == "Completed":
        return "Completed"

    today = date.today()
    difference = (due_date - today).days

    if difference < 0:
        return f"⚠️ Overdue by {abs(difference)} day(s)"

    if difference == 0:
        return "🔥 Due today"

    if difference == 1:
        return "⏰ Due tomorrow"

    if difference <= 7:
        return f"📅 Due in {difference} days"

    return f"📅 Due on {due_date.strftime('%d %b %Y')}"


def complete_assignment(index):

    assignment = st.session_state.assignments[index]

    if assignment["status"] != "Completed":

        assignment["status"] = "Completed"
        assignment["completed_at"] = date.today()

        # Award XP only once
        if not assignment.get("xp_awarded", False):

            assignment["xp_awarded"] = True

            st.session_state.xp += 30
            st.session_state.completed_assignments += 1

            st.session_state.activity.insert(
                0,
                {
                    "message": f"Completed assignment: {assignment['title']}",
                    "points": 30
                }
            )

            st.session_state.activity = (
                st.session_state.activity[:10]
            )

        return True

    return False


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="page-title">📝 Assignment Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Keep track of assignments, deadlines and your academic workload.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# OVERVIEW
# =========================================================

total = len(st.session_state.assignments)

completed = sum(
    1
    for assignment in st.session_state.assignments
    if assignment["status"] == "Completed"
)

in_progress = sum(
    1
    for assignment in st.session_state.assignments
    if assignment["status"] == "In Progress"
)

pending = sum(
    1
    for assignment in st.session_state.assignments
    if assignment["status"] == "Not Started"
)

overdue = sum(
    1
    for assignment in st.session_state.assignments
    if (
        assignment["status"] != "Completed"
        and assignment["due_date"] < date.today()
    )
)

st.subheader("📊 Assignment Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📚 Total", total)

with col2:
    st.metric("⏳ Pending", pending)

with col3:
    st.metric("🔄 In Progress", in_progress)

with col4:
    st.metric("⚠️ Overdue", overdue)


# =========================================================
# ADD ASSIGNMENT
# =========================================================

st.subheader("➕ Add New Assignment")

with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:

        title = st.text_input(
            "Assignment Title *",
            placeholder="Example: Chemistry Record"
        )

        subject = st.selectbox(
            "Subject",
            [
                "Physics",
                "Chemistry",
                "Mathematics",
                "Computer Science",
                "English",
                "Biology"
            ]
        )

        due_date = st.date_input(
            "Due Date",
            value=date.today() + timedelta(days=7)
        )

    with col2:

        description = st.text_area(
            "Description (Optional)",
            placeholder="Add any instructions, topics or notes..."
        )

        priority = st.selectbox(
            "Priority (Optional)",
            ["Low", "Medium", "High"],
            index=1
        )

        estimated_time = st.number_input(
            "Estimated Time (Optional)",
            min_value=0,
            max_value=999,
            value=0,
            step=15,
            help="Enter approximate time in minutes."
        )

    st.write("")

    if st.button(
        "➕ ADD ASSIGNMENT",
        use_container_width=True
    ):

        if not title.strip():

            st.error("Please enter an assignment title.")

        else:

            new_assignment = {
                "title": title.strip(),
                "subject": subject,
                "due_date": due_date,
                "description": description.strip(),
                "priority": priority,
                "estimated_time": estimated_time,
                "status": "Not Started",
                "created_at": date.today(),
                "completed_at": None,
                "xp_awarded": False
            }

            st.session_state.assignments.append(
                new_assignment
            )

            st.success(
                f"✅ '{title}' added successfully!"
            )


# =========================================================
# FILTERS
# =========================================================

st.subheader("🔎 Find Assignments")

col1, col2, col3 = st.columns(3)

with col1:
    status_filter = st.selectbox(
        "Status",
        ["All", "Not Started", "In Progress", "Completed"],
        index=0
    )

with col2:
    subject_options = ["All Subjects"] + sorted(
        list(set(a["subject"] for a in st.session_state.assignments))
    )
    subject_filter = st.selectbox(
        "Subject",
        subject_options,
        index=0
    )

with col3:
    priority_filter = st.selectbox(
        "Priority",
        ["All", "High", "Medium", "Low"],
        index=0
    )


# =========================================================
# FILTER ASSIGNMENTS
# =========================================================

filtered_assignments = []

for index, assignment in enumerate(
    st.session_state.assignments
):

    if (
        status_filter != "All"
        and assignment["status"] != status_filter
    ):
        continue

    if (
        subject_filter != "All Subjects"
        and assignment["subject"] != subject_filter
    ):
        continue

    if (
        priority_filter != "All"
        and assignment["priority"] != priority_filter
    ):
        continue

    filtered_assignments.append(
        (index, assignment)
    )


# =========================================================
# ASSIGNMENT LIST
# =========================================================

st.subheader("📋 My Assignments")

if not filtered_assignments:

    with st.container(border=True):

        if total == 0:

            st.info(
                "You don't have any assignments yet. "
                "Add your first assignment above! 📚"
            )

        else:

            st.info(
                "No assignments match your current filters."
            )

else:

    # Sort incomplete assignments first,
    # then by due date.
    filtered_assignments.sort(
        key=lambda item: (
            item[1]["status"] == "Completed",
            item[1]["due_date"]
        )
    )

    for index, assignment in filtered_assignments:

        status = assignment["status"]
        due_text = get_due_text(
            assignment["due_date"],
            status
        )

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            # -------------------------------------------------
            # ASSIGNMENT INFORMATION
            # -------------------------------------------------

            with col1:

                st.markdown(
                    f"### {get_status_icon(status)} "
                    f"{assignment['title']}"
                )

                st.markdown(
                    f"**{assignment['subject']}**  •  "
                    f"{get_priority_icon(assignment['priority'])} "
                    f"{assignment['priority']} Priority"
                )

                if assignment["description"]:

                    st.write(
                        assignment["description"]
                    )

                if status == "Completed":

                    st.markdown(
                        '<span class="completed">'
                        '✅ Completed'
                        '</span>',
                        unsafe_allow_html=True
                    )

                elif assignment["due_date"] < date.today():

                    st.markdown(
                        f'<span class="overdue">'
                        f'{due_text}'
                        f'</span>',
                        unsafe_allow_html=True
                    )

                elif (
                    assignment["due_date"] - date.today()
                ).days <= 3:

                    st.markdown(
                        f'<span class="due-soon">'
                        f'{due_text}'
                        f'</span>',
                        unsafe_allow_html=True
                    )

                else:

                    st.write(
                        due_text
                    )

                if assignment["estimated_time"] > 0:

                    st.caption(
                        f"⏱️ Estimated time: "
                        f"{assignment['estimated_time']} minutes"
                    )

            # -------------------------------------------------
            # ACTIONS
            # -------------------------------------------------

            with col2:

                if status != "Completed":

                    new_status = st.selectbox(
                        "Status",
                        ["Not Started", "In Progress", "Completed"],
                        index=["Not Started", "In Progress", "Completed"].index(status),
                        key=f"status_{index}"
                    )

                    if new_status != status:

                        if new_status == "Completed":
                            completed_now = complete_assignment(index)
                            if completed_now:
                                st.success("🎉 +30 XP")
                        else:
                            assignment["status"] = new_status
                        

                else:
                    st.success("Completed ✓")

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{index}",
                    use_container_width=True
                ):

                    st.session_state.assignments.pop(
                        index
                    )


# =========================================================
# COMPLETION PROGRESS
# =========================================================

st.subheader("📈 Completion Progress")

if total > 0:

    completion_percentage = completed / total

    with st.container(border=True):

        st.write(
            f"**{completed} of {total} assignments completed**"
        )

        st.progress(
            completion_percentage
        )

        st.caption(
            f"{completion_percentage * 100:.0f}% complete"
        )

else:

    with st.container(border=True):

        st.info(
            "Your completion progress will appear here "
            "once you add assignments."
        )


# =========================================================
# UPCOMING DEADLINES
# =========================================================

st.subheader("📅 Upcoming Deadlines")

upcoming = []

for assignment in st.session_state.assignments:

    if assignment["status"] in ["Not Started", "In Progress"]:

        days_left = (
            assignment["due_date"] - date.today()
        ).days

        if 0 <= days_left <= 7:

            upcoming.append(
                (days_left, assignment)
            )

upcoming.sort(
    key=lambda item: item[0]
)

if upcoming:

    for days_left, assignment in upcoming[:5]:

        if days_left == 0:
            timing = "🔥 Due today"
        elif days_left == 1:
            timing = "⏰ Due tomorrow"
        else:
            timing = f"📅 {days_left} days left"

        st.write(
            f"**{assignment['title']}** "
            f"— {assignment['subject']} "
            f"— {timing}"
        )

else:

    st.info(
        "No deadlines in the next 7 days. 🎉"
    )


# =========================================================
# GAMIFICATION NOTE
# =========================================================

st.divider()

with st.container(border=True):

    st.markdown("### 🏆 Your Progress Counts")

    st.write(
        "Completing an assignment earns **30 XP**."
    )

    st.caption(
        "XP is awarded only once for each assignment. "
    )


# =========================================================
# NAVIGATION
# =========================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "← BACK TO DASHBOARD",
        use_container_width=True
    ):

        st.switch_page(
            "pages/dashboard1.py"
        )

with col2:

    if st.button(
        "🏆 VIEW GAMIFICATION",
        use_container_width=True
    ):

        st.switch_page(
            "pages/6_gamification.py"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "✨ Stay organized • Meet deadlines • Complete your goals"
)
