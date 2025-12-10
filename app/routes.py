from flask import render_template, request, redirect, session
from random import choice
from app import app, db
from app.models import Question

# Module names mapping
MODULE_NAMES = {
    2: "Installing Motherboards & Connectors",
    3: "Installing System Devices",
    4: "Troubleshooting PC Hardware",
    5: "Comparing Local Networking Hardware",
    6: "Configuring Addressing & Internet Connections",
    7: "Supporting Network Services",
    8: "Summarizing Virtualization & Cloud Concepts",
    9: "Supporting Mobile Devices",
    10: "Supporting Print Devices"
}

# Home Page Route
@app.route('/')
def index():
    # Clear progress-related session variables
    session.pop("all_question_ids", None)
    session.pop("answered_questions", None)
    session.pop("current_question_number", None)
    session.pop("total_questions", None)
    session.pop("correct_answers", None)
    session.pop("selected_modules", None)

    # Get all unique modules from the database
    modules = sorted([m[0] for m in db.session.query(Question.module).distinct().all()])
    
    # Create list of module info with names
    modules_with_names = [{"number": m, "name": MODULE_NAMES.get(m, f"Module {m}")} for m in modules]
    
    return render_template('index.html', modules=modules_with_names, module_names=MODULE_NAMES)


# Question Route
@app.route('/question', methods=["GET", "POST"])
def question():
    # Handle module selection from POST request
    if request.method == "POST":
        selected_modules = request.form.getlist("modules")
        if not selected_modules:
            # No modules selected, redirect back to index with error message
            modules = sorted([m[0] for m in db.session.query(Question.module).distinct().all()])
            modules_with_names = [{"number": m, "name": MODULE_NAMES.get(m, f"Module {m}")} for m in modules]
            return render_template('index.html', modules=modules_with_names, module_names=MODULE_NAMES, error="Please select at least one module.")
        
        # Convert to integers and store in session
        selected_modules = [int(m) for m in selected_modules]
        session["selected_modules"] = selected_modules
        
        # Get question IDs for selected modules
        questions = Question.query.filter(Question.module.in_(selected_modules)).all()
        session["all_question_ids"] = [q.id for q in questions]
        session["answered_questions"] = []
        session["current_question_number"] = 0
        session["total_questions"] = 0
        session["correct_answers"] = 0
    
    # Check if modules are selected
    if "selected_modules" not in session or not session["selected_modules"]:
        return redirect("/")
    
    # Initialize all session variables if not already present
    if "all_question_ids" not in session:
        # Fallback: if no modules selected, redirect to index
        return redirect("/")
    if "answered_questions" not in session:
        session["answered_questions"] = []  # Track answered questions
    if "current_question_number" not in session:
        session["current_question_number"] = 0  # Start question counter

    all_question_ids = session["all_question_ids"]
    answered_questions = session["answered_questions"]

    # Get the next random question
    remaining_questions = list(set(all_question_ids) - set(answered_questions))
    if not remaining_questions:
        return redirect("/final_results")  # No questions left, show results

    random_question_id = choice(remaining_questions)  # Randomize
    question = Question.query.get(random_question_id)

    # Add this question to answered list and increment counter
    answered_questions.append(random_question_id)
    session["answered_questions"] = answered_questions
    session["current_question_number"] += 1  # Increment the question counter

    # Calculate progress
    total_questions = len(all_question_ids)
    current_question_number = session["current_question_number"]
    questions_left = total_questions - current_question_number
    progress_percentage = int((current_question_number / total_questions) * 100)

    return render_template(
        "question.html",
        question=question,
        total_questions=total_questions,
        current_question_number=current_question_number,
        questions_left=questions_left,
        progress_percentage=progress_percentage,
    )

# Check Answer Route
@app.route('/check_answer', methods=['POST'])
def check_answer():
    question_id = int(request.form.get("question_id"))
    selected_answers = request.form.getlist("answers")
    question = Question.query.get(question_id)

    # Check if the selected answers match the correct answers
    correct_answers = [answer.strip().lower() for answer in question.correct_answers.split("|")]
    selected_answers = [answer.strip().lower() for answer in selected_answers]

    # Determine if the answers are correct
    is_correct = set(selected_answers) == set(correct_answers)

    # Initialize session variables if they don't exist
    if "total_questions" not in session:
        session["total_questions"] = 0
        session["correct_answers"] = 0

    # Increment the total question count
    session["total_questions"] += 1

    # Increment the correct answer count if the answer is correct
    if is_correct:
        session["correct_answers"] += 1

    # Check if there are more questions
    remaining_questions = list(
        set(session["all_question_ids"]) - set(session["answered_questions"])
    )
    if remaining_questions:
        return render_template(
            "result.html",  # Updated template name
            is_correct=is_correct,
            correct_answers=question.correct_answers.split("|"),
            next_question_url="/question",
        )
    else:
        # All questions are complete
        percentage = int((session["correct_answers"] / session["total_questions"]) * 100)
        return render_template(
            "final_results.html",
            correct=session["correct_answers"],
            total=session["total_questions"],
            percentage=percentage,
        )


# Reset Progress Route
@app.route("/reset", methods=["GET"])
def reset():
    session.pop("all_question_ids", None)
    session.pop("answered_questions", None)
    session.pop("total_questions", None)
    session.pop("correct_answers", None)
    session.pop("selected_modules", None)
    session.pop("current_question_number", None)
    return redirect("/")

# Final Results Route
@app.route('/final_results', methods=["GET"])
def final_results():
    return render_template("final_results.html")
