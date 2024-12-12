from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")),  # Path to templates
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))  # Path to static files
)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/questions.db'  # Database path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
app.secret_key = "your_secret_key"  # Required for session management

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes to register them with the app
from app import routes
