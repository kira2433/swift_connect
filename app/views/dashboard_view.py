from flask import render_template, request, session
from app.core.database import *
from flask import Blueprint, render_template 

dashboard_bp = Blueprint('dashboard', __name__)
 
def get_current_user():
    user_id = session.get("user_id")
    db = connect_to_database()
    if user_id:
        cursor = execute_query(db, "SELECT * FROM users WHERE id = %s", (session["user_id"],))
        user = fetch_one(cursor)
        current_user = {
            'id':user[0],
            'username':user[1], 
            'email':user[2],
            'role':user[4]
        }
        return current_user 
    else:
        return {"current_user": None}   
    

@dashboard_bp.route('/')
def dashboard_page():
    db = connect_to_database() 
    print(str(session["user_id"]))
    print(str(session["username"]))
    print(str(session["role"]))    
    print("from dashboard: " + str(session["username"]))
    current_user = get_current_user()
    print(str(current_user))

    cursor = execute_query(db, "SELECT * FROM connection_requests")
    connection_requests = fetch_all(cursor)
    close_database_connection(db)
    request_dicts = []  # Create an empty list to store dictionaries
    for row in connection_requests:
        request_dict = {
            "id": row[0],  # Assuming "id" is the first column
            "customer_id": row[1],
            "swift_address": row[2],
            "end_user_details": row[3],
            "platform_integration_details": row[4],
            "submitted_at": row[5].strftime("%Y-%m-%d %H:%M:%S")  # Format date
        }
        # Add more key-value pairs as needed based on your table columns
        request_dicts.append(request_dict)

    context = {"connection_requests": request_dicts}

    # Print for debugging (remove in production)
    print(connection_requests)
    print(context)
    return render_template("dashboard.html", current_user=current_user, context=context)


@dashboard_bp.route('/<int:request_id>')
def request_details(request_id):
    # Fetch request details from the database based on request_id
    # Render the request details template with the fetched data
    return render_template('request_details.html', request_id=request_id)
