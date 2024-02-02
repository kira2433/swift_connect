from flask import render_template, request, redirect, url_for, session
from app.core.database import *
from app.views.dashboard_view import get_current_user
from flask import Blueprint, render_template

request_bp = Blueprint('request', __name__)

@request_bp.route('/')
def request_page():
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
            "id": row[0],  
            "customer_id": row[1],
            "swift_address": row[2],
            "end_user_details": row[3],
            "platform_integration_details": row[4],
            "submitted_at": row[5].strftime("%Y-%m-%d %H:%M:%S")  # Format date
        }
        # Add more key-value pairs as needed based on your table columns
        request_dicts.append(request_dict)

    context = {"connection_requests": request_dicts}

    # Print for debugging  
    print(connection_requests)
    print(context)
    return render_template("request_dashboard.html", current_user=current_user, context=context)

 
@request_bp.route('/new', methods=["GET"])
def new_request_form():
    try:
        return render_template("request_form.html" )
    except Exception as e: 
        return render_template("error.html", error_message="An error occurred while fetching requests.")  
 

@request_bp.route('/<int:request_id>')
def view_request_details(request_id):
    db = connect_to_database()
    cursor = execute_query(db, "SELECT * FROM connection_requests WHERE id = %s", (request_id,))
    request = fetch_one(cursor)
    close_database_connection(db)
    return render_template("request_details.html", request=request)

def edit_request(request_id):
    # Retrieve request data from the database
    # Render the request form with pre-filled data
    pass

@request_bp.route("/process_form", methods=["POST"])  # Handle only POST requests
def process_form():
    try: 
        user_id = session.get("user_id")
        print("user"+str(user_id)) 
        swift_address = request.form["swift_address"]
        end_user_details = request.form["end_user_details"]
        platform_integration_details = request.form["platform_integration_details"]
        db = connect_to_database()
        # Prepare the SQL query with placeholders for security
        query = """
            INSERT INTO connection_requests (
                customer_id, swift_address, end_user_details, platform_integration_details
            ) VALUES (%s, %s, %s, %s)
        """
        cursor = execute_query(db, "INSERT INTO connection_requests (customer_id, swift_address, end_user_details, platform_integration_details) VALUES (%s, %s, %s, %s)", (user_id, swift_address, end_user_details, platform_integration_details))
        close_database_connection(db)

        # Redirect to a success page  
        return redirect(url_for("dashboard.dashboard_page"))  # Replace with your desired success route

    except Exception as e:
        # error handling
        handle_database_error(e)
        return render_template("error.html", error_message="An error occurred while processing the request.")

 

# ... other view functions with similar database interactions and validation
