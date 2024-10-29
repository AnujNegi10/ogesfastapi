# OGES FastAPI and Streamlit Project

## Overview
This project is a web application developed using FastAPI for the backend and Streamlit for the frontend. It provides user registration/signup and login functionality 

## Features
- User registration with validation
- User login with session management
- Welcome page after login
- Error handling for invalid credentials and duplicate emails

## Requirements
- Python 3.7 or higher
- pip (Python package installer)
- A database (e.g., SQLite, PostgreSQL, MySQL)

## Getting Started

### Clone the Repository
Clone this repository to your local machine using the following command:

git clone https://github.com/AnujNegi10/ogesfastapi.git
cd ogesfastapi

## Install Dependencies

- pip install -r requirements.txt

## Set Up the Database

- Set Up the Database , using SQLite, the database file will be created automatically

## Update Database Connection Settings

- DATABASE_URL = "sqlite:///./test.db" (Do Accordingly)

## Run the FastAPI Backend

- uvicorn blog.main:app --reload

## Run the Streamlit Frontend

- streamlit run frontend.py

## Access the Application

## Feel free to adjust any specific details, such as the database connection string or the structure of your project, as needed.
