import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from PyPDF2 import PdfReader
from openai import OpenAI

# Load OpenAI client using the environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/generate-quiz", methods=["POST"])
def generate_quiz():
    try:
        data = request.get_json()
        files = data.get("files", [])
        question_type = data.get("question_type", "MCQ")
        num_questions = data.get("num_questions", 5)

        # Combine text from all uploaded PDFs
        all_text = ""
        for hex_file in files:
            file_bytes = bytes.fromhex(hex_file)
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    all_text += extracted_text + "\n"

        if not all_text.strip():
            return jsonify({"error": "No extractable text found in uploaded PDFs."}), 400

        # Build prompt
        prompt = (
            f"Based on the following study material, generate {num_questions} {question_type} quiz questions. "
            f"Study Material:\n{all_text[:3000]}"  # Truncate to avoid token overflow
        )

        # Generate quiz using new OpenAI SDK
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates quiz questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        quiz = response.choices[0].message.content
        return jsonify({"quiz": quiz})

    except Exception as e:
        print("🔥 Error in /generate-quiz:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
