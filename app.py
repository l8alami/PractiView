from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Ensure the upload directory exists
upload_directory = os.path.join('backend', 'uploads')
os.makedirs(upload_directory, exist_ok=True)

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/')
def home():
    return redirect(url_for('start'))

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/submit', methods=['POST'])
def submit():
    resume_file = request.files.get('resume')
    if resume_file and resume_file.filename != '':
        # Secure filename check can be added here if needed
        filepath = os.path.join(upload_directory, resume_file.filename)
        resume_file.save(filepath)
        return redirect(url_for("success"))
    else:
        return "Resume file not provided.", 400

@app.route('/success')
def success():
    return render_template('contact.html')

@app.route('/hareth', methods=['GET', 'POST'])
def hareth():
    if request.method == 'POST':
        # Process the form data here
        user_input = request.form.get('user_input')
        # You can now use user_input for further processing or pass it to the template
        return render_template('index.html', user_input=user_input)
    return render_template('index.html')

@app.route('/evaluate-answer', methods=['POST'])
def evaluate_answer():
    # Get the answer from the form
    answer = request.form['user_answer']
    # Here you would typically process the answer, evaluate it, etc.

    # Render the evaluation page with any necessary data
    return render_template('evaluation.html', answer=answer)


