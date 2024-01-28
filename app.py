from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    # Get the job description from the form
    job_description = request.form.get('job_description')
    
    # Get the uploaded resume file
    resume_file = request.files['resume']

    # Check if the resume file is provided
    if resume_file:
        # Save the job description to a text file
        with open(os.path.join('backend/uploads', 'job_description.txt'), 'w') as text_file:
            text_file.write(job_description)
        
        # Save the resume file to the uploads directory
        resume_file.save(os.path.join('backend/uploads', resume_file.filename))
        return redirect(url_for("success"))
        return "Form submitted successfully."
    else:
        return "Resume file not provided."
@app.route('/success')
def success():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
