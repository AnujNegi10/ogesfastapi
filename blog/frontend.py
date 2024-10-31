import streamlit as st
import requests
import time
import re

# FastAPI base URL
FASTAPI_URL = "https://ogesfastapi-1.onrender.com"

# Initialize session state for login status and token
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.username = ""
    st.session_state.token = ""

# Function to validate password
def validate_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"\d", password)):
        return False
    return True

# Function to register a new user
def register_user():
    st.title("Oges Sign Up Page")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Sign Up"):
        if not username.strip() or not email.strip() or not password.strip():
            st.warning("Please fill in all fields to sign up.")
        elif not validate_password(password):
            st.warning("Password must be at least 8 characters long, include at least one uppercase letter and one number.")
        else:
            payload = {"name": username, "email": email, "password": password}
            try:
                response = requests.post(f"{FASTAPI_URL}/user", json=payload)
                response.raise_for_status()
                st.success("User registered successfully!")
            except requests.RequestException:
                st.error("Failed to register user. Please try again.")

# Function to login a user
def login_user():
    st.title("Oges Login Page")
    username = st.text_input("Email")  # Using email for login
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not username.strip() or not password.strip():
            st.warning("Please enter both username and password to log in.")
        else:
            payload = {"username": username, "password": password}
            try:
                response = requests.post(f"{FASTAPI_URL}/login", data=payload)
                response.raise_for_status()
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.session_state.token = response.json().get("access_token")
                st.success("Logged in successfully!")
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 404:
                    st.error("User not found. Please sign up first.")
                elif err.response.status_code == 401:
                    st.error("Incorrect password. Please try again.")
                else:
                    st.error("Failed to log in. Please try again.")

# Function to display welcome page after login
def welcome_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.markdown("""
    At OGES, we have a unique combination of Oil & Gas domain experts, software engineers, 
    and recruitment experts. This combination has helped us to develop multiple Digital Solutions 
    for the Oil & Gas industry.
    """)
    
    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.success("You have been logged out.")

# Streamlit app logic
if st.session_state.is_logged_in:
    welcome_page()
else:
    option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Sign Up":
        register_user()
    elif option == "Login":
        login_user()
