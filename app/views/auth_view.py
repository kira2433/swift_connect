from flask import render_template, request, redirect, session, flash, url_for 
from app.core.database import *
from app import app
from flask import Blueprint
auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/')
def login():
    return render_template('login.html')


@auth_blueprint.route('/', methods=['POST'])
def login_user():
    username = request.form["username"]
    password = request.form["password"]

    db = connect_to_database()
    cursor = execute_query(db, "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = fetch_one(cursor)
    close_database_connection(db)

    if user:
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["role"] = user[4]
        return redirect("/dashboard")
    else:
        flash("Invalid username or password.", "error")
        return redirect("/")


@auth_blueprint.route('/register', methods=['POST'])
def register(self, app):
    # Implement user registration logic, password hashing, and database insertion 
    username = request.form["username"]
    password = request.form["password"]

    # Hash the password securely
    hashed_password = generate_password_hash(password)  # Replace with your hashing function

    db = connect_to_database()
    cursor = execute_query(db, "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", (username, hashed_password, "customer"))
    close_database_connection(db)

    # Redirect to login or success page
    return redirect("/")  

@auth_blueprint.route('/logout')
def logout():
    session.clear()  # Invalidate the session to log the user out
    return redirect("/")  # Redirect to login page

def generate_password_hash(password):
    return password
