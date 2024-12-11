from app import app
import datetime
import os

def log_usage(route_name):
    log_file_path = os.path.join(os.path.dirname(__file__), "../usage_log.txt")  # Adjust path to the root directory
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{datetime.datetime.now()} - Route Accessed: {route_name}\n")

if __name__ == '__main__':
    app.run(debug=True)
