import streamlit as st
import requests

# FastAPI base URL
FASTAPI_URL = "http://127.0.0.1:8000"

# Initialize session state
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.username = ""
    st.session_state.token = ""

# Function to register a new user
def register_user():
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        payload = {"name": username, "email": email, "password": password}
        response = requests.post(f"{FASTAPI_URL}/user", json=payload)
        if response.status_code == 200:
            st.success("User registered successfully!")
        else:
            st.error("Failed to register user")

# Function to login a user
def login_user():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Use FastAPI's login endpoint to get token
        payload = {"username": email, "password": password}
        response = requests.post(f"{FASTAPI_URL}/login", data=payload)
        if response.status_code == 200:
            st.session_state.is_logged_in = True
            st.session_state.username = email
            st.session_state.token = response.json().get("access_token")
            st.success("Logged in successfully!")
        else:
            st.error("Invalid email or password")

# Function to display welcome page after login
def welcome_page():
    st.title(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""

# Streamlit app logic
if st.session_state.is_logged_in:
    welcome_page()
else:
    option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Sign Up":
        register_user()
    elif option == "Login":
        login_user()
