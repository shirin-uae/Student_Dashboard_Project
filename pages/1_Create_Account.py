import streamlit as st
from auth import create_account

st.set_page_config(
    page_title="Create Account",
    page_icon="🎓",
    layout="centered"
)
# Hide Streamlit's automatic page navigation
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)
st.title("🎓 Create Account")
st.write("Create your account to get started.")

st.divider()

name = st.text_input("Full Name")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("CREATE ACCOUNT", use_container_width=True):

    if not name or not username or not password or not confirm_password:
        st.error("Please fill in all the fields.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:
        success, message = create_account(
            username,
            password,
            name
        )

        if success:
            st.success(message)
            st.info("You can now sign in.")

            if st.button("GO TO SIGN IN →"):
                st.switch_page("app.py")

        else:
            st.error(message)

st.divider()

st.write("Already have an account?")

if st.button("Sign in →"):
    st.switch_page("app.py")
