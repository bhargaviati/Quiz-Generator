from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import PyPDF2
import io

app = Flask(__name__)
CORS(app)

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    data = request.json
    files = data.get("files", [])
    question_type = data.get("question_type", "MCQ")
    num_questions = int(data.get("num_questions", 5))

    full_text = ""
    for file_content in files:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(bytes.fromhex(file_content)))
        for page in pdf_reader.pages:
            full_text += page.extract_text()

    prompt = f"Generate {num_questions} {question_type} questions from this text:\n{full_text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }]
    )
    return jsonify({"quiz": response.choices[0].message.content})
