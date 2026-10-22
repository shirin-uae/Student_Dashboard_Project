import streamlit as st
import json
import mysql.connector

from database import get_connection


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="AI Student Dashboard",
    page_icon="🎓",
    layout="wide"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

    [data-testid="stSidebarNav"] {
        display: none;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .hero-subtitle {
        color: #777;
        font-size: 17px;
        margin-top: 5px;
    }

    .feature-title {
        font-size: 21px;
        font-weight: 650;
    }

    .feature-description {
        color: #666;
        min-height: 60px;
    }

</style>
""", unsafe_allow_html=True)


# =========================
# LOGGED-IN USER
# =========================

username = st.session_state.get("username")


if not username:

    st.error("Please sign in first.")
    st.stop()


# =========================
# LOAD STUDENT FROM MYSQL
# =========================

def load_student():

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                name,
                class_name,
                section,
                stream,
                subjects
            FROM students
            WHERE username = %s
            """,
            (username,)
        )

        return cursor.fetchone()

    except mysql.connector.Error as e:

        st.error(f"Database error: {e}")
        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


student = load_student()


if not student:

    st.error("Student account could not be found.")
    st.stop()


# =========================
# STUDENT INFORMATION
# =========================

student_name = student["name"] or "Student"

class_name = student["class_name"] or "12"

section = student["section"] or "A"

stream = student["stream"] or "Science"


subjects = []

if student["subjects"]:

    try:

        subjects = json.loads(student["subjects"])

    except (json.JSONDecodeError, TypeError):

        subjects = []


# =========================
# GAMIFICATION DATA
# =========================

xp = st.session_state.get("xp", 0)

streak = st.session_state.get("streak", 0)


# =========================
# HEADER
# =========================

st.markdown(
    '<div class="hero-title">🎓 AI Student Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Your intelligent academic companion'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================
# WELCOME
# =========================

st.markdown(
    f"## Welcome back, {student_name}! 👋"
)

st.write(
    "Manage your academics, stay organized, track your progress "
    "and build better study habits."
)


# =========================
# OVERVIEW
# =========================

st.subheader("📊 Your Overview")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎓 Class",
        f"{class_name} - {section}"
    )


with col2:

    st.metric(
        "📚 Stream",
        stream
    )


with col3:

    st.metric(
        "📖 Subjects",
        len(subjects)
    )


with col4:

    st.metric(
        "🏆 XP",
        xp
    )


# =========================
# ACADEMIC TOOLS
# =========================

st.subheader("🚀 Academic Tools")


# =========================
# ROW 1
# =========================

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-title">'
            '🧠 AI Performance'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-description">'
            'Analyze your marks, understand your academic '
            'performance and identify your strengths and areas '
            'that need improvement.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "VIEW PERFORMANCE →",
            key="performance",
            use_container_width=True
        ):

            st.switch_page(
                "pages/2_AI_Performance.py"
            )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-title">'
            '👤 Student Profile'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-description">'
            'Manage your personal information, academic details, '
            'stream and subjects.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "VIEW PROFILE →",
            key="profile",
            use_container_width=True
        ):

            st.switch_page(
                "pages/3_student_profile.py"
            )


# =========================
# ROW 2
# =========================

col1, col2 = st.columns(2)


with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-title">'
            '📅 Smart Study Planner'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-description">'
            'Organize your study sessions, plan your workload '
            'and stay on top of your academic goals.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "OPEN STUDY PLANNER →",
            key="planner",
            use_container_width=True
        ):

            st.switch_page(
                "pages/4_smart_study_planner.py"
            )


with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-title">'
            '📝 Assignment Tracker'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="feature-description">'
            'Track assignments, deadlines, priorities and '
            'completion status in one place.'
            '</div>',
            unsafe_allow_html=True
        )

        if st.button(
            "VIEW ASSIGNMENTS →",
            key="assignments",
            use_container_width=True
        ):

            st.switch_page(
                "pages/5_assignment_tracker.py"
            )


# =========================
# GAMIFICATION
# =========================

st.subheader("🏆 Your Learning Journey")

with st.container(border=True):

    col1, col2 = st.columns([2.5, 1])


    with col1:

        st.markdown("### 🏆 Gamification")

        st.write(
            "Turn your academic progress into XP, streaks, "
            "achievements and rewards."
        )

        st.caption(
            "Complete real study tasks and assignments to "
            "build your progress."
        )


    with col2:

        st.metric(
            "🔥 Current Streak",
            f"{streak} days"
        )

        if st.button(
            "VIEW GAMIFICATION →",
            key="gamification",
            use_container_width=True
        ):

            st.switch_page(
                "pages/6_gamification.py"
            )


# =========================
# QUICK ACCESS
# =========================

st.subheader("⚡ Quick Access")

col1, col2, col3, col4 = st.columns(4)


with col1:

    if st.button(
        "🧠 AI Performance",
        key="quick_performance",
        use_container_width=True
    ):

        st.switch_page(
            "pages/2_AI_Performance.py"
        )


with col2:

    if st.button(
        "📅 Study Planner",
        key="quick_planner",
        use_container_width=True
    ):

        st.switch_page(
            "pages/4_smart_study_planner.py"
        )


with col3:

    if st.button(
        "📝 Assignments",
        key="quick_assignments",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_assignment_tracker.py"
        )


with col4:

    if st.button(
        "🏆 Gamification",
        key="quick_gamification",
        use_container_width=True
    ):

        st.switch_page(
            "pages/6_gamification.py"
        )


# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "✨ Study Smarter • Stay Organized • Track Progress • Keep Improving"
)
