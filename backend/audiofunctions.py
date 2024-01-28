import os
import openai
from flask import Flask, request, jsonify
import pdfplumber
import random
from dotenv import load_dotenv
load_dotenv()

questionNumber=1

openai.api_key = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)

interview_questions = [
    "Tell me about a time when you had to meet a tight deadline.",
    "Describe a situation where you worked with a difficult coworker.",
    "Give an example of a goal you reached and how you achieved it.",
    "Tell me about a time you made a mistake and how you handled it.",
    "Describe how you have handled a challenge in the workplace.",
    "Tell me about a time when you had to go above and beyond your regular duties.",
    "Describe a situation where you had to persuade someone to see things your way.",
    "Provide an example of when you had to use your communication skills to convey a point.",
    "Tell me about a time when you had to work under significant pressure.",
    "Describe a time when you were part of a successful team and your role in it.",
    "Give an example of a time when you showed initiative at work.",
    "Tell me about a time when you had to adapt to a significant change at work.",
    "Describe a situation where you had to solve a difficult problem.",
    "Tell me about a time when you had to manage multiple responsibilities.",
    "Give an example of how you have handled a conflict with another team member.",
    "Describe a time when you took a leadership role.",
    "Tell me about a time when you had to deal with a dissatisfied customer.",
    "Give an example of a project that didn’t go as planned and how you handled it.",
    "Describe a time when you had to learn something new in a short period.",
    "Tell me about a time when you had to give someone difficult feedback."
]
resumeFilePath = "backend/uploads/resume.pdf"
jobDescription = "backend/uploads/job_description.txt"

def pdfToText(filePath):
    text = ''
    with pdfplumber.open(filePath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def introduction(resumeFilePath, jobDescription):
    # Select a random question from the list
    resumeText = pdfToText(resumeFilePath)
    index = random.randint(0, len(interview_questions) - 1)
    #question = interview_questions[index]
    questionNumber = 1

    # Construct the prompt
    prompt = f"You are an interviewer, interviewing a candidate for the job description: {jobDescription}. The interviewee has a resume: {resumeText}. Give a brief personalized hello (mention interviewee name), and begin the interview process, ask a brief introductory yet specific question about the job description"

    # OpenAI Chat completion
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )
    response_content = response.choices[0].message.content
    print(response)
    # Implement logic to create output1.mp3 (using openai texttospeech)
    generate_audio(response_content, questionNumber)
    return response_content

def generate_audio(script, number):
    # Ensure the OpenAI API key is set
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # Generate Text-to-Speech audio
    response = openai.audio.speech.create(
        model="tts-1",  # The text-to-speech model
        voice="alloy",  # The voice model (you can choose a different one if needed)
        input=script    # The input script
    )

    # Save the audio to a file
    file_name = os.path.join('static', f'output{number}.mp3')
    response.stream_to_file(file_name)
    print(f"Audio saved as {file_name}")

# Example usage
script = "This is an example script to be converted into speech."
number = 1
generate_audio(script, number)


introduction(resumeFilePath, jobDescription)