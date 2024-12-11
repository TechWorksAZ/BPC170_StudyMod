from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Explicitly configure Flask app with custom static and template folder paths
app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates")),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
)

# Manually add a static route to force Flask to recognize the correct static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    from flask import send_from_directory
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
    return send_from_directory(static_dir, filename)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes
