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
# Use instance folder for database (works on both local and Render)
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, '..', 'instance')
os.makedirs(instance_path, exist_ok=True)
database_path = os.path.join(instance_path, 'questions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_change_in_production')  # Required for session management

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes to register them with the app
from app import routes
