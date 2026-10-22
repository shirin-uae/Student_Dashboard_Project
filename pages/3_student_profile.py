import streamlit as st
import json
from datetime import date
from database import get_connection

st.set_page_config(
    page_title="Student Profile",
    page_icon="👤",
    layout="wide"
)

# Hide Streamlit's automatic page navigation
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# LOGIN CHECK
# ─────────────────────────────────────────

username = st.session_state.get("username")

if not username:
    st.error("Please sign in first.")
    st.stop()


# ─────────────────────────────────────────
# STREAMS & SUBJECTS
# ─────────────────────────────────────────


STREAM_SUBJECTS = {
    "PCMC": [
        "Physics",
        "Chemistry",
        "Mathematics",
        "Computer Science",
        "English"
    ],

    "PCMB": [
        "Physics",
        "Chemistry",
        "Mathematics",
        "Biology",
        "English"
    ],

    "PCBP": [
        "Physics",
        "Chemistry",
        "Psychology",
        "Biology",
        "English"
    ]
}

STREAM_OPTIONS = list(STREAM_SUBJECTS.keys())



GENDER_OPTIONS = [
    "Prefer not to say",
    "Female",
    "Male",
    "Other"
]


# ─────────────────────────────────────────
# LOAD PROFILE
# ─────────────────────────────────────────

def load_profile():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                username, name, class_name, section,
                academic_year, gender, stream, subjects,
                date_of_birth, email, phone
            FROM students
            WHERE username = %s
        """, (username,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


profile = load_profile()

if not profile:
    st.error("Student profile could not be found.")
    st.stop()


# ─────────────────────────────────────────
# SAVED VALUES
# ─────────────────────────────────────────

student_name = profile["name"] or "Your Name"
saved_class = str(profile["class_name"] or "12")
saved_section = profile["section"] or "A"
saved_year = profile["academic_year"] or ""
saved_gender = profile["gender"] or "Prefer not to say"

# Do NOT default to Humanities or Science.
# If there is no valid saved stream, the user must choose one.
saved_stream = profile["stream"] if profile["stream"] in STREAM_OPTIONS else None

saved_email = profile["email"] or ""
saved_phone = profile["phone"] or ""

saved_dob = profile["date_of_birth"] or date(2008, 1, 1)

try:
    saved_subjects = json.loads(profile["subjects"]) if profile["subjects"] else []
except (json.JSONDecodeError, TypeError):
    saved_subjects = []


# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────

st.title("👤 Student Profile")
st.caption("View and manage your personal and academic information.")

st.divider()

st.subheader(f"Welcome, {student_name}! 👋")

with st.container(border=True):
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("""
        <div style="
            width:120px;
            height:120px;
            border-radius:50%;
            background:#f0f2f6;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:55px;
            margin:auto;
        ">👤</div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"### {student_name}")
        st.write(f"**Username:** {username}")
        st.write("**Student Account:** Active")


# ─────────────────────────────────────────
# PERSONAL INFORMATION
# ─────────────────────────────────────────

st.subheader("📋 Personal Information")

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Full Name",
            value=student_name,
            disabled=True
        )

        date_of_birth = st.date_input(
            "Date of Birth",
            value=saved_dob
        )

        gender = st.selectbox(
            "Gender",
            GENDER_OPTIONS,
            index=(
                GENDER_OPTIONS.index(saved_gender)
                if saved_gender in GENDER_OPTIONS else 0
            )
        )

    with col2:
        email = st.text_input(
            "Email Address",
            value=saved_email
        )

        phone = st.text_input(
            "Phone Number",
            value=saved_phone
        )


# ─────────────────────────────────────────
# ACADEMIC INFORMATION
# ─────────────────────────────────────────

st.subheader("🎓 Academic Information")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        class_options = ["11", "12"]

        class_name = st.selectbox(
            "Class",
            class_options,
            index=(
                class_options.index(saved_class)
                if saved_class in class_options else 1
            )
        )

    with col2:
        section_options = ["A", "B", "C", "D", "E"]

        section = st.selectbox(
            "Section",
            section_options,
            index=(
                section_options.index(saved_section)
                if saved_section in section_options else 0
            )
        )

    with col3:
        if saved_stream in STREAM_OPTIONS:
            stream_index = STREAM_OPTIONS.index(saved_stream)
        else:
            stream_index = 0

        stream = st.selectbox(
            "Stream",
            STREAM_OPTIONS,
            index=stream_index
        )

    academic_year = st.text_input(
        "Academic Year",
        value=saved_year,
        placeholder="Example: 2026-2027"
    )


# ─────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────

st.subheader("📚 Subjects")

# Get subjects according to selected stream
available_subjects = STREAM_SUBJECTS[stream]

# Only keep subjects that belong to the selected stream
valid_saved_subjects = [
    subject for subject in saved_subjects
    if subject in available_subjects
]

selected_subjects = st.multiselect(
    f"Select your {stream} subjects",
    available_subjects,
    default=valid_saved_subjects
)

if selected_subjects:
    st.write("**Selected Subjects:**")
    st.write(" • " + "\n • ".join(selected_subjects))
else:
    st.info(
        f"Select the subjects you are studying in the {stream} stream."
    )


# ─────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────

def save_profile():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE students
            SET
                name = %s,
                class_name = %s,
                section = %s,
                academic_year = %s,
                gender = %s,
                stream = %s,
                subjects = %s,
                date_of_birth = %s,
                email = %s,
                phone = %s
            WHERE username = %s
        """, (
            student_name,
            class_name,
            section,
            academic_year,
            gender,
            stream,
            json.dumps(selected_subjects),
            date_of_birth,
            email,
            phone,
            username
        ))

        connection.commit()

        # Update session state
        st.session_state["name"] = student_name
        st.session_state["class"] = class_name
        st.session_state["section"] = section
        st.session_state["stream"] = stream
        st.session_state["subjects"] = selected_subjects
        st.session_state["academic_year"] = academic_year

        return True

    except Exception as e:
        connection.rollback()
        st.error(f"Could not save profile: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


# ─────────────────────────────────────────
# BUTTONS
# ─────────────────────────────────────────

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 SAVE PROFILE", use_container_width=True):
        if save_profile():
            st.success("Profile information saved successfully!")

with col2:
    if st.button("← BACK TO DASHBOARD", use_container_width=True):
        st.switch_page("pages/dashboard1.py")

st.divider()

st.caption("✨ Keep your profile updated for a better personalized experience.")
