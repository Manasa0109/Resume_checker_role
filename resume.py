import os
import streamlit as st
import pdfplumber
from openai import OpenAI
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key="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"  
)
st.title("📄 AI Resume ATS Checker")
st.write("Upload your resume and ask questions like 'Is this good for a respective role?'")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        resume_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"
        st.session_state.resume_text = resume_text
    st.success("✅ Resume successfully uploaded and parsed.")
user_question = st.text_input("Ask your resume-related question:")
if st.button("Submit Question") and st.session_state.resume_text and user_question.strip():
    full_prompt = f"This is my resume:\n{st.session_state.resume_text}\n\n{user_question}"
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert ATS and career advisor. Help the user assess and improve their resume. And also give how much relatable my resume for the role i mentioned.For 100 points and also give missing skills for the role i mentioned. and generate pdf format of new version."},
                {"role": "user", "content": full_prompt}
            ],
            model="meta/Meta-Llama-3.1-8B-Instruct",
            temperature=0.7,
            max_tokens=2048,
            top_p=0.9,
        )
        st.subheader("🤖 AI Response")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error from model: {e}")
