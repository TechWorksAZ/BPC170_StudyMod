import sys
import os

# Add the project root directory to sys.path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory (data/)
project_root = os.path.abspath(os.path.join(current_dir, '..'))  # Go up one level to the project root
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app import db, app  # Import Flask app and database
from app.models import Question  # Import the Question model
import csv

# Path to the CSV file
file_path = os.path.join(current_dir, "questions.csv")

# Ensure the database and tables are created
with app.app_context():
    db.create_all()  # Creates the database and the `question` table if it doesn't exist
    print("Database and tables created successfully!")

# Clear existing data in the database
with app.app_context():
    db.session.query(Question).delete()  # Deletes all rows in the 'question' table
    db.session.commit()
    print("Database cleared successfully!")

# Populate the database with data from the CSV file
with app.app_context():
    with open(file_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if a question with this ID already exists
            question = db.session.get(Question, row['id'])

            if question:
                # Update the existing question
                question.module = row['module']
                question.question = row['question']
                question.correct_answers = row['correct_answers']
                question.choices = row['choices']
                question.image_url = row['image_url']
            else:
                # Add a new question
                question = Question(
                    id=int(row['id']),
                    module=row['module'],
                    question=row['question'],
                    correct_answers=row['correct_answers'],
                    choices=row['choices'],
                    image_url=row['image_url'],
                )
                db.session.add(question)
        db.session.commit()
        print("Database populated successfully!")
