import streamlit as st
import requests

st.title("📘 AI Quiz Generator")

backend_url = "https://quiz-generator-ugbd.onrender.com/generate-quiz"

uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
question_type = st.selectbox("Select Question Type", ["MCQ", "True/False", "Short Answer"])
num_questions = st.slider("Number of Questions", 1, 20, 5)

if st.button("Generate Quiz"):
    if uploaded_files:
        file_contents = []
        for file in uploaded_files:
            content = file.read()
            file_contents.append(content.hex())

        with st.spinner("Generating..."):
            try:
                res = requests.post(backend_url, json={
                    "files": file_contents,
                    "question_type": question_type,
                    "num_questions": num_questions
                })

                if res.status_code == 200:
                    st.markdown("### ✅ Generated Quiz")
                    st.write(res.json()["quiz"])
                else:
                    st.error(f"Something went wrong. Status Code: {res.status_code}")
                    st.write(res.text)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please upload at least one PDF.")
