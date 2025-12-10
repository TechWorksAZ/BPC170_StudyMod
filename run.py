from app import app
import datetime
import os

def log_usage(route_name):
    log_file_path = os.path.join(os.path.dirname(__file__), "../usage_log.txt")  # Adjust path to the root directory
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - Route Accessed: {route_name}\n")

if __name__ == '__main__':
    # For local development
    app.run(debug=True)
else:
    # For production (gunicorn)
    # Ensure database is populated on first run
    from app import db
    from app.models import Question
    with app.app_context():
        if db.session.query(Question).count() == 0:
            print("Database is empty, populating...")
            import subprocess
            subprocess.run(["python", "data/populate_db.py"], check=True)
