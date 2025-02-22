import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret123'  # Required for session management

# Sample 10 questions
questions = [
    {"question": "What comes next in the sequence?", "sequence": ["🔴", "🟢", "🔵", "🔴", "?"], "options": {"A": "🟢", "B": "🔵", "C": "🔴"}, "answer": "C"},
    {"question": "Find the missing shape", "sequence": ["⬛", "⬜", "⬛", "⬜", "?"], "options": {"A": "⬜", "B": "⬛", "C": "🟥"}, "answer": "A"},
    {"question": "Which color comes next?", "sequence": ["🔵", "🔴", "🔵", "🔴", "?"], "options": {"A": "🔵", "B": "🟢", "C": "🔴"}, "answer": "A"},
    {"question": "Choose the next pattern", "sequence": ["⭐", "🌙", "⭐", "🌙", "?"], "options": {"A": "⭐", "B": "🌙", "C": "☀️"}, "answer": "A"},
    {"question": "What comes next?", "sequence": ["🍎", "🍊", "🍎", "🍊", "?"], "options": {"A": "🍌", "B": "🍎", "C": "🍊"}, "answer": "B"},
    {"question": "Select the missing number", "sequence": ["2", "4", "6", "8", "?"], "options": {"A": "10", "B": "12", "C": "14"}, "answer": "A"},
    {"question": "Which letter comes next?", "sequence": ["A", "C", "E", "G", "?"], "options": {"A": "H", "B": "I", "C": "J"}, "answer": "B"},
    {"question": "Identify the missing animal", "sequence": ["🐶", "🐱", "🐶", "🐱", "?"], "options": {"A": "🐶", "B": "🐭", "C": "🐰"}, "answer": "A"},
    {"question": "Find the missing symbol", "sequence": ["❤️", "💙", "❤️", "💙", "?"], "options": {"A": "💛", "B": "❤️", "C": "💙"}, "answer": "B"},
    {"question": "Which shape comes next?", "sequence": ["🔺", "🔵", "🔺", "🔵", "?"], "options": {"A": "🔺", "B": "🔵", "C": "⚫"}, "answer": "A"},
      {"question": "Select the next pattern in the sequence:", "sequence": ["⬛", "⚫", "⬛", "?"], "options": {"square": "⬛ Square", "circle": "⚫ Circle"}, "answer": "circle"},
    {"question": "Which shape comes next?", "sequence": ["🔺", "🔵", "🔺", "?"], "options": {"triangle": "🔺 Triangle", "circle": "🔵 Circle"}, "answer": "circle"},
    {"question": "Pick the correct pattern:", "sequence": ["🟢", "🟡", "🟢", "?"], "options": {"green": "🟢 Green", "yellow": "🟡 Yellow"}, "answer": "yellow"},
    {"question": "What comes next?", "sequence": ["🟥", "🟨", "🟥", "?"], "options": {"red": "🟥 Red", "yellow": "🟨 Yellow"}, "answer": "yellow"},
    {"question": "Identify the pattern:", "sequence": ["🔶", "🔷", "🔶", "?"], "options": {"diamond": "🔷 Diamond", "hexagon": "🔶 Hexagon"}, "answer": "diamond"},
    {"question": "Next shape?", "sequence": ["🔵", "🔴", "🔵", "?"], "options": {"blue": "🔵 Blue", "red": "🔴 Red"}, "answer": "red"},
    {"question": "Complete the sequence:", "sequence": ["⬜", "⬛", "⬜", "?"], "options": {"white": "⬜ White", "black": "⬛ Black"}, "answer": "black"},
    {"question": "What follows?", "sequence": ["🟧", "🟦", "🟧", "?"], "options": {"orange": "🟧 Orange", "blue": "🟦 Blue"}, "answer": "blue"},
    {"question": "Guess the missing shape:", "sequence": ["🟠", "🟣", "🟠", "?"], "options": {"purple": "🟣 Purple", "orange": "🟠 Orange"}, "answer": "purple"},
    {"question": "Find the next pattern:", "sequence": ["⬜", "⬛", "⬛", "⬜", "⬜", "?"], "options": {"black": "⬛ Black", "white": "⬜ White"}, "answer": "black"},
    {"question": "What is the missing shape?", "sequence": ["🔺", "🔻", "🔺", "?"], "options": {"up": "🔺 Up Triangle", "down": "🔻 Down Triangle"}, "answer": "down"},
    {"question": "Choose the correct pattern:", "sequence": ["🟥", "🟩", "🟦", "?"], "options": {"blue": "🟦 Blue", "green": "🟩 Green"}, "answer": "green"},
    {"question": "Complete the set:", "sequence": ["🟤", "⚪", "🟤", "?"], "options": {"white": "⚪ White", "brown": "🟤 Brown"}, "answer": "white"},
    {"question": "Identify the missing pattern:", "sequence": ["🟪", "🟨", "🟪", "?"], "options": {"yellow": "🟨 Yellow", "purple": "🟪 Purple"}, "answer": "yellow"},
    {"question": "Which shape continues the pattern?", "sequence": ["🟢", "🟠", "🟢", "?"], "options": {"green": "🟢 Green", "orange": "🟠 Orange"}, "answer": "orange"}
]

@app.route('/')
def home():
    """Start the quiz with random 5 questions"""
    session.clear()  # Clear session for a new quiz
    session['question_order'] = random.sample(range(len(questions)), 5)  # Select 5 random questions
    session['current_question'] = 0  # Start from first question
    session['user_answers'] = []  # Store user answers
    return redirect(url_for('question'))

@app.route('/question', methods=['GET', 'POST'])
def question():
    """Handles quiz question display and answer submission"""
    
    if 'question_order' not in session or len(session['question_order']) == 0:
        return redirect(url_for('home'))  # Restart quiz if session is empty
    
    current_index = session.get('current_question', 0)

    # If all questions are answered, go to results
    if current_index >= len(session['question_order']):
        return redirect(url_for('result'))

    if request.method == 'POST':
        user_choice = request.form.get('answer')
        question_index = session['question_order'][current_index]
        correct_answer = questions[question_index]['answer']

        session['user_answers'].append({"selected": user_choice, "correct": correct_answer})
        session['current_question'] += 1  # Move to next question
        return redirect(url_for('question'))

    # Get current question
    question_index = session['question_order'][session['current_question']]
    return render_template("index.html", question=questions[question_index], 
                           index=session['current_question'] + 1, total=len(session['question_order']))

@app.route('/result')
def result():
    """Displays quiz results"""
    user_answers = session.get('user_answers', [])
    score = sum(1 for ans in user_answers if ans["selected"] == ans["correct"])
    return render_template("result.html", score=score, total=len(session['question_order']), user_answers=user_answers)

if __name__ == '__main__':
    app.run(debug=True)