from venv import logger
import mysql.connector
import os
import logging
import smtplib
from email.mime.text import MIMEText

def connect_to_database():
    # Establish connection using your database credentials
    try:
        host = os.environ.get("DB_HOST", "127.0.0.1")
        user = os.environ.get("DB_USER", "root")
        password = os.environ.get("DB_PASSWORD", "root")
        database = os.environ.get("DB_DATABASE", "swift_connect")

        db = mysql.connector.connect(
            host=host,
            user=user,
            port=3336, 
            password=password,
            database=database
        )
        return db
    except mysql.connector.Error as err:
        print("Database connection error:", err)
        return None  # Or raise an exception for further handling
    return db

def execute_query(db, query, params=None):
    cursor = db.cursor()
    cursor.execute(query, params)
    if query.lower().startswith("select"):  # Check for SELECT queries
        results = cursor  # Fetch the results
        return results  # Return the fetched results
    else:
        db.commit()  # Commit for non-SELECT queries
    return cursor
 
def fetch_all(cursor):
    return cursor.fetchall()

def fetch_one(cursor):
    return cursor.fetchone()

def close_database_connection(db):
    db.close()

def handle_database_error(error):
    """Handles database-related errors."""
    logger.error("Database error occurred: %s", error, exc_info=True)  # Log the error with traceback
    # Optional: Notify administrators via email or other channels
    send_error_notification(error)
    # If using database transactions, roll back any incomplete operations
    # if transaction_open():
    #     transaction.rollback()
    # Return a suitable response to the user (e.g., redirect to error page) 

def send_error_notification(error):
    """Sends an email notification about a database error."""
    recipient_email = "admin@example.com"
    message = MIMEText("A database error has occurred:\n\nError Type: {}\nMessage: {}\n".format(type(error), error))
    message['Subject'] = "Database Error Alert"
    message['From'] = "your_app_email_address@example.com"
    message['To'] = recipient_email

    # with smtplib.SMTP("your_smtp_server", port=587) as server:
    #     server.starttls()
    #     server.login("your_smtp_username", "your_smtp_password")
    #     server.send_message(message)