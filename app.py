"""
app.py - Sign-in page (the entry point of the project).
Run with:  streamlit run app.py
"""
import streamlit as st
from auth import login_user

st.set_page_config(page_title="AI Student Dashboard - Sign In",
                   page_icon="🎓", layout="centered")

# Hide Streamlit's automatic page navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 AI Student Dashboard")
st.write("Sign in to continue.")
st.divider()

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("SIGN IN", use_container_width=True):
    if not username or not password:
        st.error("Please enter your username and password.")
    else:
        student = login_user(username, password)
        if student:
            # These keys are read by every other page
            st.session_state["student_id"] = student["id"]
            st.session_state["username"] = student["username"]
            st.session_state["name"] = student["name"]
            st.switch_page("pages/dashboard1.py")
        else:
            st.error("Incorrect username or password.")

st.divider()
st.write("New here?")
if st.button("Create an account →"):
    st.switch_page("pages/1_Create_Account.py")
