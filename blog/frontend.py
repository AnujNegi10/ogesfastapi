import streamlit as st
import requests
import time
import re  # Import regular expressions module

# FastAPI base URL
FASTAPI_URL = "https://ogesfastapi-1.onrender.com"

# Initialize session state for login status and token
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
    st.session_state.username = ""
    st.session_state.token = ""

# Add an image at the top of the app with a specific width
# st.image(r"C:\Users\negia\Downloads\logo.png", width=200, use_column_width=False)  # Set width to 200 pixels

# Function to validate password
def validate_password(password):
    if (len(password) < 8 or  # Minimum length
        not re.search(r"[A-Z]", password) or  # At least one uppercase letter
        not re.search(r"\d", password)):  # At least one number
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
                response.raise_for_status()  # Raise an error for bad responses
                st.success("User registered successfully!")
            except requests.RequestException:
                st.error("Failed to register user. Please try again.")

# Function to login a user
def login_user():
    st.title("Oges Login Page")
    username = st.text_input("Email")  # FastAPI's OAuth2PasswordRequestForm uses 'username' to pass email
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not username.strip() or not password.strip():
            st.warning("Please enter both username and password to log in.")
        else:
            payload = {"username": username, "password": password}
            try:
                response = requests.post(f"{FASTAPI_URL}/login", data=payload)
                response.raise_for_status()  # Raise an error for bad responses
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.session_state.token = response.json().get("access_token")
                st.success("Logged in successfully!")
                display_timed_message("Double tap to log in!")  # Display timed message
            except requests.RequestException:
                st.error("Invalid username or password. Please try again.")

# Function to display a timed message
def display_timed_message(message):
    message_placeholder = st.empty()  # Create an empty placeholder for the message
    message_placeholder.warning(message)  # Show the message
    time.sleep(3)  # Wait for 3 seconds
    message_placeholder.empty()  # Clear the message

# Function to display welcome page after login
def welcome_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.markdown("""
    At OGES, we have a unique combination of Oil & Gas domain experts, software engineers, 
    and recruitment experts. This combination has helped us to develop multiple Digital Solutions 
    for the Oil & Gas industry.
    """)  # Use Markdown for better formatting
    
    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        st.success("You have been logged out.")
        display_timed_message("Double tap to log out!")  # Display timed message

# Streamlit app logic
if st.session_state.is_logged_in:
    welcome_page()
else:
    option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
    if option == "Sign Up":
        register_user()
    elif option == "Login":
        login_user()
