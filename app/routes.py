from flask import render_template, request, jsonify
from app import app, db
from app.models import Question

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/question')
def get_question():
    question = Question.query.order_by(db.func.random()).first()  # Fetch a random question
    return render_template('question.html', question=question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    # Get form data from the request
    selected_answers = request.form.getlist('answers')  # User-selected answers
    question_id = request.form.get('question_id')  # Hidden input for question ID

    # Fetch the question from the database
    question = Question.query.get(question_id)
    correct_answers = set(answer.strip() for answer in question.correct_answers.split('|'))  # Correct answers as a set

    # Strip and process user-selected answers
    selected_answers = set(answer.strip() for answer in selected_answers)

    # Compare the sets
    is_correct = selected_answers == correct_answers

    # Return the result to the user
    return render_template(
        'result.html',
        is_correct=is_correct,
        correct_answers=list(correct_answers)  # Pass correct answers as a list for display
    )

@app.route('/debug_static_path')
def debug_static_path():
    import os
    static_path = os.path.join(app.root_path, "static")
    return f"Static Path: {static_path}, Exists: {os.path.exists(static_path)}"

@app.route('/debug_root')
def debug_root():
    import os
    return f"Root Path: {app.root_path}"
