from backend.audiofunctions import introduction
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

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
    if resume_file and allowed_file(resume_file.filename):
        # Save the resume file
        filepath = os.path.join(upload_directory, 'resume.pdf')
        resume_file.save(filepath)

        # Call the introduction function from audiofunctions.py
        jobDescriptionPath = os.path.join(upload_directory, 'job_description.txt')
        introduction(filepath, jobDescriptionPath)

        # Store the path of the audio file in the session
        session['audio_file'] = 'output1.mp3'  # No need for 'backend/uploads' as it's in 'static'

        return redirect(url_for("success"))
    else:
        return "Resume file not provided or file type not allowed.", 400

def allowed_file(filename):
    # Check if the file has one of the allowed extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'doc', 'docx'}

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio_data' in request.files:
        audio_file = request.files['audio_data']
        # Save the file as 'response1.mp3' in the backend/uploads directory
        filepath = os.path.join(upload_directory, 'response1.mp3')
        audio_file.save(filepath)
        return jsonify({'message': 'File uploaded successfully!'})
    return jsonify({'error': 'No file part'}), 400


@app.route('/success')
def success():
    # Get the audio file path from the session
    audio_file = session.get('audio_file', None)
    return render_template('contact.html', audio_file=audio_file)

@app.route('/hareth', methods=['GET', 'POST'])
def hareth():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        return render_template('index.html', user_input=user_input)
    return render_template('index.html')

@app.route('/evaluate-answer', methods=['POST'])
def evaluate_answer():
    answer = request.form['user_answer']
    return render_template('evaluation.html', answer=answer)

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False in production
