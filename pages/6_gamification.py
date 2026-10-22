import streamlit as st
from datetime import date, timedelta


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Gamification",
    page_icon="🏆",
    layout="wide"
)

# Hide Streamlit's automatic page navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #777;
        font-size: 17px;
        margin-bottom: 20px;
    }

    .level-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #f7f7f7;
        text-align: center;
    }

    .badge {
        padding: 15px;
        border-radius: 15px;
        background-color: #f7f7f7;
        text-align: center;
        min-height: 150px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "completed_study_sessions" not in st.session_state:
    st.session_state.completed_study_sessions = 0

if "completed_assignments" not in st.session_state:
    st.session_state.completed_assignments = 0

if "completed_goals" not in st.session_state:
    st.session_state.completed_goals = 0

if "completed_revisions" not in st.session_state:
    st.session_state.completed_revisions = 0

if "last_study_date" not in st.session_state:
    st.session_state.last_study_date = None

if "activity" not in st.session_state:
    st.session_state.activity = []

if "claimed_rewards" not in st.session_state:
    st.session_state.claimed_rewards = []


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def add_activity(message, points):
    st.session_state.xp += points

    st.session_state.activity.insert(
        0,
        {
            "message": message,
            "points": points
        }
    )

    # Keep only the latest 10 activities
    st.session_state.activity = st.session_state.activity[:10]


def get_level(xp):
    levels = [
        (0, 1, "🌱 Beginner"),
        (100, 2, "📚 Learner"),
        (250, 3, "🔥 Rising Scholar"),
        (500, 4, "🧠 Knowledge Builder"),
        (800, 5, "⭐ Academic Achiever"),
        (1200, 6, "🏆 Scholar"),
        (1700, 7, "💎 Master Learner"),
        (2500, 8, "👑 Elite Student"),
    ]

    current = levels[0]

    for level in levels:
        if xp >= level[0]:
            current = level
        else:
            break

    return current


def get_next_level(xp):
    thresholds = [100, 250, 500, 800, 1200, 1700, 2500]

    for threshold in thresholds:
        if xp < threshold:
            return threshold

    return None


def mark_study_today():
    today = date.today()
    last_date = st.session_state.last_study_date

    if last_date == today:
        return False, "You've already marked today's study session."

    if last_date == today - timedelta(days=1):
        st.session_state.streak += 1
    else:
        st.session_state.streak = 1

    st.session_state.last_study_date = today

    return True, f"🔥 Your streak is now {st.session_state.streak} day(s)!"


# ---------------------------------------------------------
# ACHIEVEMENTS
# ---------------------------------------------------------

def get_achievements():

    xp = st.session_state.xp
    streak = st.session_state.streak
    study_sessions = st.session_state.completed_study_sessions
    assignments = st.session_state.completed_assignments
    goals = st.session_state.completed_goals

    return [
        {
            "name": "First Step",
            "icon": "🌱",
            "description": "Complete your first study activity.",
            "unlocked": len(st.session_state.activity) >= 1
        },
        {
            "name": "Getting Started",
            "icon": "📚",
            "description": "Earn 100 XP.",
            "unlocked": xp >= 100
        },
        {
            "name": "Study Machine",
            "icon": "⚡",
            "description": "Complete 5 study sessions.",
            "unlocked": study_sessions >= 5
        },
        {
            "name": "Assignment Ace",
            "icon": "📝",
            "description": "Complete 5 assignments.",
            "unlocked": assignments >= 5
        },
        {
            "name": "Goal Crusher",
            "icon": "🎯",
            "description": "Complete 5 daily goals.",
            "unlocked": goals >= 5
        },
        {
            "name": "3-Day Momentum",
            "icon": "🔥",
            "description": "Reach a 3-day study streak.",
            "unlocked": streak >= 3
        },
        {
            "name": "Week Warrior",
            "icon": "🏅",
            "description": "Reach a 7-day study streak.",
            "unlocked": streak >= 7
        },
        {
            "name": "Scholar",
            "icon": "🧠",
            "description": "Earn 500 XP.",
            "unlocked": xp >= 500
        },
        {
            "name": "Elite Student",
            "icon": "👑",
            "description": "Earn 1200 XP.",
            "unlocked": xp >= 1200
        }
    ]


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

student_name = st.session_state.get("name", "Student")

st.markdown(
    '<div class="main-title">🏆 Gamification</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Turn your study progress into achievements, rewards and momentum.</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------------------------------------------------
# LEVEL + XP
# ---------------------------------------------------------

level_start, level_number, level_title = get_level(st.session_state.xp)
next_level = get_next_level(st.session_state.xp)

st.subheader("🌟 Your Progress")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "⭐ XP",
        st.session_state.xp
    )

with col2:
    st.metric(
        "🏆 Level",
        f"Level {level_number}"
    )

with col3:
    st.metric(
        "🔥 Study Streak",
        f"{st.session_state.streak} days"
    )

with col4:
    unlocked_count = sum(
        1 for achievement in get_achievements()
        if achievement["unlocked"]
    )

    st.metric(
        "🏅 Achievements",
        unlocked_count
    )


with st.container(border=True):

    st.markdown(f"### {level_title}")

    if next_level is not None:

        current_level_xp = level_start
        progress = (
            (st.session_state.xp - current_level_xp)
            / (next_level - current_level_xp)
        )

        progress = max(0.0, min(progress, 1.0))

        st.progress(progress)

        remaining = next_level - st.session_state.xp

        st.caption(
            f"{remaining} XP needed to reach the next level."
        )

    else:
        st.progress(1.0)
        st.caption("🎉 You've reached the highest level!")


# ---------------------------------------------------------
# EARN XP
# ---------------------------------------------------------

st.subheader("⚡ Earn XP")

st.write(
    "Complete real study activities to earn points and build your academic streak."
)

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.markdown("### 📖 Study Session")
        st.write("Complete a focused study session.")

        if st.button(
            "COMPLETE STUDY SESSION  +20 XP",
            use_container_width=True
        ):
            st.session_state.completed_study_sessions += 1

            add_activity(
                "Completed a study session",
                20
            )

            st.success("🎉 +20 XP earned!")


    with st.container(border=True):

        st.markdown("### 📝 Assignment")
        st.write("Complete an assignment.")

        if st.button(
            "COMPLETE ASSIGNMENT  +30 XP",
            use_container_width=True
        ):
            st.session_state.completed_assignments += 1

            add_activity(
                "Completed an assignment",
                30
            )

            st.success("🎉 +30 XP earned!")


with col2:

    with st.container(border=True):

        st.markdown("### 🎯 Daily Goal")
        st.write("Complete one of your daily academic goals.")

        if st.button(
            "COMPLETE DAILY GOAL  +25 XP",
            use_container_width=True
        ):
            st.session_state.completed_goals += 1

            add_activity(
                "Completed a daily goal",
                25
            )

            st.success("🎯 +25 XP earned!")


    with st.container(border=True):

        st.markdown("### 🧠 Revision")
        st.write("Complete a revision or practice session.")

        if st.button(
            "COMPLETE REVISION  +15 XP",
            use_container_width=True
        ):
            st.session_state.completed_revisions += 1

            add_activity(
                "Completed a revision session",
                15
            )

            st.success("🧠 +15 XP earned!")


# ---------------------------------------------------------
# DAILY STREAK
# ---------------------------------------------------------

st.subheader("🔥 Daily Streak")

with st.container(border=True):

    col1, col2 = st.columns([2, 1])

    with col1:

        st.markdown(
            f"### {st.session_state.streak} Day Streak 🔥"
        )

        if st.session_state.streak == 0:
            st.write(
                "Start studying today to begin your streak!"
            )
        elif st.session_state.streak < 3:
            st.write(
                "Keep going! You're building momentum."
            )
        elif st.session_state.streak < 7:
            st.write(
                "You're on fire! Keep the momentum going."
            )
        else:
            st.write(
                "Amazing consistency! You're a study warrior."
            )

    with col2:

        if st.button(
            "🔥 MARK TODAY AS STUDIED",
            use_container_width=True
        ):

            success, message = mark_study_today()

            if success:
                st.success(message)
            else:
                st.info(message)


# ---------------------------------------------------------
# ACHIEVEMENTS
# ---------------------------------------------------------

st.subheader("🏅 Achievements")

achievements = get_achievements()

for i in range(0, len(achievements), 3):

    cols = st.columns(3)

    for j, col in enumerate(cols):

        index = i + j

        if index >= len(achievements):
            break

        achievement = achievements[index]

        with col:

            with st.container(border=True):

                if achievement["unlocked"]:

                    st.markdown(
                        f"## {achievement['icon']}"
                    )

                    st.markdown(
                        f"### {achievement['name']}"
                    )

                    st.write(
                        achievement["description"]
                    )

                    st.success("UNLOCKED ✓")

                else:

                    st.markdown("## 🔒")

                    st.markdown(
                        f"### {achievement['name']}"
                    )

                    st.write(
                        achievement["description"]
                    )

                    st.caption("Locked")


# ---------------------------------------------------------
# REWARDS
# ---------------------------------------------------------

st.subheader("🎁 Rewards")

rewards = [
    {
        "name": "Bronze Scholar",
        "icon": "🥉",
        "xp": 100,
        "description": "Your first major milestone."
    },
    {
        "name": "Silver Scholar",
        "icon": "🥈",
        "xp": 250,
        "description": "You're building serious momentum."
    },
    {
        "name": "Gold Scholar",
        "icon": "🥇",
        "xp": 500,
        "description": "You've become a consistent learner."
    },
    {
        "name": "Elite Scholar",
        "icon": "👑",
        "xp": 1200,
        "description": "You've reached elite academic status."
    }
]

for i in range(0, len(rewards), 2):

    cols = st.columns(2)

    for j, col in enumerate(cols):

        index = i + j

        if index >= len(rewards):
            break

        reward = rewards[index]

        with col:

            with st.container(border=True):

                st.markdown(
                    f"## {reward['icon']} {reward['name']}"
                )

                st.write(
                    reward["description"]
                )

                if st.session_state.xp >= reward["xp"]:

                    if reward["name"] in st.session_state.claimed_rewards:

                        st.success("✓ REWARD CLAIMED")

                    else:

                        if st.button(
                            f"CLAIM REWARD • {reward['xp']} XP",
                            key=f"reward_{reward['xp']}",
                            use_container_width=True
                        ):

                            st.session_state.claimed_rewards.append(
                                reward["name"]
                            )

                            st.success(
                                f"🎉 {reward['name']} unlocked!"
                            )

                else:

                    remaining = reward["xp"] - st.session_state.xp

                    st.progress(
                        min(
                            st.session_state.xp / reward["xp"],
                            1.0
                        )
                    )

                    st.caption(
                        f"🔒 {remaining} XP more needed"
                    )


# ---------------------------------------------------------
# RECENT ACTIVITY
# ---------------------------------------------------------

st.subheader("📈 Recent Activity")

if st.session_state.activity:

    with st.container(border=True):

        for item in st.session_state.activity:

            col1, col2 = st.columns([5, 1])

            with col1:
                st.write(
                    f"✨ {item['message']}"
                )

            with col2:
                st.write(
                    f"**+{item['points']} XP**"
                )

else:

    with st.container(border=True):
        st.info(
            "No activity yet. Complete a study activity above to start earning XP!"
        )


# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

st.subheader("📊 Your Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📖 Study Sessions",
        st.session_state.completed_study_sessions
    )

with col2:
    st.metric(
        "📝 Assignments",
        st.session_state.completed_assignments
    )

with col3:
    st.metric(
        "🎯 Goals",
        st.session_state.completed_goals
    )

with col4:
    st.metric(
        "🧠 Revisions",
        st.session_state.completed_revisions
    )


# ---------------------------------------------------------
# MOTIVATION
# ---------------------------------------------------------

st.divider()

with st.container(border=True):

    if st.session_state.streak >= 7:

        st.markdown(
            "### 👑 You're building an incredible habit!"
        )
        st.write(
            "Consistency beats intensity. Keep showing up."
        )

    elif st.session_state.xp >= 500:

        st.markdown(
            "### ⭐ You're doing seriously well!"
        )
        st.write(
            "Your progress is adding up. Keep pushing forward."
        )

    elif st.session_state.xp >= 100:

        st.markdown(
            "### 🔥 You're gaining momentum!"
        )
        st.write(
            "Every study session gets you closer to your goals."
        )

    else:

        st.markdown(
            "### 🌱 Every journey starts with one step."
        )
        st.write(
            "Complete your first study activity and start building your academic streak."
        )


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

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
        "📅 GO TO STUDY PLANNER",
        use_container_width=True
    ):
        st.switch_page(
            "pages/4_smart_study_planner.py"
        )


# ---------------------------------------------------------
# TESTING / RESET
# ---------------------------------------------------------

with st.expander("⚙️ Testing Options"):

    st.write(
        "Use this only while testing the gamification system."
    )

    if st.button("Reset Gamification Progress"):

        st.session_state.xp = 0
        st.session_state.streak = 0
        st.session_state.completed_study_sessions = 0
        st.session_state.completed_assignments = 0
        st.session_state.completed_goals = 0
        st.session_state.completed_revisions = 0
        st.session_state.last_study_date = None
        st.session_state.activity = []
        st.session_state.claimed_rewards = []

        st.success("Gamification progress has been reset.")
        st.rerun()


st.caption(
    "✨ Study Smarter • Build Consistency • Earn Achievements • Keep Improving"
)

