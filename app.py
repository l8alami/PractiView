from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='templates', static_folder='static')


#app = Flask(__name__)
CORS(app)

# Your routes here

if __name__ == '__main__':
    app.run(debug=True)

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
    # Get the uploaded resume file
    resume_file = request.files.get('resume')

    # Check if the resume file is provided
    if resume_file and resume_file.filename != '':
        # Process the resume file here
        # For example, save the file
        resume_file.save(os.path.join('backend/uploads', resume_file.filename))

        # Redirect to the success page
        return redirect(url_for("success"))
    else:
        # Return an error message if no file is provided
        return "Resume file not provided."


@app.route('/success')
def success():
    return render_template('contact.html')

@app.route('/hareth', methods=['POST'])
def hareth():
    user_input = request.form.get('user_input')
    print(user_input)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
