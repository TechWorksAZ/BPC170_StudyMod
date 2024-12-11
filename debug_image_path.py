from app import db, app
from app.models import Question

with app.app_context():  # Set up the application context
    questions = Question.query.all()
    for question in questions:
        print(f"ID: {question.id}, Image URL: {question.image_url}")
