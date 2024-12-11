from app import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(500), nullable=False)
    correct_answers = db.Column(db.String(500), nullable=False)  # Comma-separated correct answers
    choices = db.Column(db.String(500), nullable=False)  # Pipe-separated choices
    image_url = db.Column(db.String(500), nullable=True)  # Optional image URL
