import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random 24-byte key
# Import your views here
from app.views import auth_view, dashboard_view, request_view
# Import your blueprints here
from app.views.auth_view import auth_blueprint
from app.views.dashboard_view import dashboard_bp
from app.views.request_view import request_bp

# Register your blueprints here
app.register_blueprint(auth_blueprint )
# app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
# app.register_blueprint(dashboard_bp )
app.register_blueprint(request_bp, url_prefix='/request')
