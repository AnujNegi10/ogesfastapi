import streamlit as st
import requests
import re
import time

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

# Function to validate email
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Function to display a pop-up message
def display_message(message, message_type="info"):
    if message_type == "success":
        st.success(message)
    elif message_type == "error":
        st.error(message)
    elif message_type == "warning":
        st.warning(message)

# Function to register a new user
def register_user():
    st.title("Oges Sign Up Page")
    username = st.text_input("Username", placeholder="Enter your username")
    email = st.text_input("Email", placeholder="e.g. john@gmail.com")  # Added placeholder
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Sign Up"):
        if not username.strip() or not email.strip() or not password.strip():
            st.warning("Please fill in all fields to sign up.")
        elif not validate_password(password):
            st.warning("Password must be at least 8 characters long, include at least one uppercase letter and one number.")
        elif not validate_email(email):
            st.warning("Please enter a valid email address.")
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
    username = st.text_input("Email", placeholder="e.g. john@gmail.com")  # Added placeholder
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if not username.strip() or not password.strip():
            display_message("Please enter both username and password to log in.", "warning")
        elif not validate_email(username):
            display_message("Please enter a valid email address.", "warning")
        else:
            payload = {"username": username, "password": password}
            try:
                response = requests.post(f"{FASTAPI_URL}/login", data=payload)
                response.raise_for_status()
                st.session_state.is_logged_in = True
                st.session_state.username = username
                st.session_state.token = response.json().get("access_token")

                # Show success message and hint to double-click to login
                display_message("Logged in successfully!", "success")
                time.sleep(1)  # Delay to allow user to see success message
                st.warning("Double click to login.")

            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 404:
                    display_message("User not found. Please sign up first.", "error")
                elif err.response.status_code == 401:
                    display_message("Incorrect password. Please try again.", "error")
                else:
                    display_message("Failed to log in. Please try again.", "error")

# Function to display welcome page after login
def welcome_page():
    st.title(f"Welcome, {st.session_state.username}!")
    st.markdown(""" At OGES, we have a unique combination of Oil & Gas domain experts, software engineers, 
    and recruitment experts. This combination has helped us to develop multiple Digital Solutions 
    for the Oil & Gas industry.
    """)
    
    if st.button("Logout"):
        st.session_state.is_logged_in = False
        st.session_state.username = ""
        st.session_state.token = ""
        display_message("You have been logged out.", "success")

# Streamlit app logic
def main():
    # Custom CSS for styling
    st.markdown(
        """
        <style>
            .main {
                background-color: #f0f0f5;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .logo {
                text-align: center;
            }
            .logo img {
                width: 150px;
                height: auto;
            }
            h1 {
                color: #2c3e50;
            }
            .stButton {
                background-color: #2980b9;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-size: 16px;
            }
            .stButton:hover {
                background-color: #3498db;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Logo section
    st.markdown("<div class='logo'><img src='https://oges.co/images/logo.png' alt='Logo'></div>", unsafe_allow_html=True)

    if st.session_state.is_logged_in:
        welcome_page()
    else:
        option = st.sidebar.selectbox("Choose an option", ["Login", "Sign Up"])
        if option == "Sign Up":
            register_user()
        elif option == "Login":
            login_user()

if __name__ == "__main__":
    main()
