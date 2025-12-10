from app import app, db
import datetime
import os

def log_usage(route_name):
    log_file_path = os.path.join(os.path.dirname(__file__), "../usage_log.txt")  # Adjust path to the root directory
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - Route Accessed: {route_name}\n")

# Initialize database and populate if needed
def init_db():
    """Create tables and populate database if empty"""
    with app.app_context():
        # Create all tables first - this is critical!
        db.create_all()
        print("Database tables created/verified")
        
        # Check if database needs to be populated
        from app.models import Question
        try:
            # Use a try-except to handle the case where table doesn't exist yet
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if 'question' not in inspector.get_table_names():
                print("Question table doesn't exist, creating...")
                db.create_all()
            
            count = db.session.query(Question).count()
            if count == 0:
                print("Database is empty, populating...")
                import subprocess
                import sys
                script_path = os.path.join(os.path.dirname(__file__), "data", "populate_db.py")
                result = subprocess.run([sys.executable, script_path], check=False, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"Warning: populate_db.py exited with code {result.returncode}")
                    print(f"Error output: {result.stderr}")
                else:
                    print("Database populated successfully!")
        except Exception as e:
            print(f"Error checking/populating database: {e}")
            print("Attempting to populate database...")
            import subprocess
            import sys
            script_path = os.path.join(os.path.dirname(__file__), "data", "populate_db.py")
            result = subprocess.run([sys.executable, script_path], check=False, capture_output=True, text=True)
            if result.returncode == 0:
                print("Database populated successfully!")
            else:
                print(f"Failed to populate: {result.stderr}")

# Initialize database on import (for production with gunicorn)
# This ensures tables exist before the app starts serving requests
if __name__ != '__main__':
    init_db()

if __name__ == '__main__':
    # For local development
    init_db()
    app.run(debug=True)
