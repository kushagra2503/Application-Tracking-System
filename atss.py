import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load gemini model
def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

input_prompt="""
Hey act like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering data,data science,sata analyst and
big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competetive and you should provide 
best assistance for improving the resumes. Assign the percentage matching based
on jd and 
the missing keywords with high accuracy
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"JD Match":"%","Missing KeyWords:[]","Profile Summary":""}}

At last tell me if the applicant is suitable for this job role based on the Jd match if the percentage is greater than 70%
"""

# Streamlit app
st.title("Smart ATS")
st.subheader("Improve Your Resume ATS Score")

jd = st.text_area("Paste the Job Description Here:")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload a PDF file")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and jd:
        resume_text = input_pdf_text(uploaded_file)
        
        # Fill input prompt with actual resume text and job description
        prompt = input_prompt.format(text=resume_text, jd=jd)
        response = get_gemini_response(prompt)
        
        st.subheader("ATS Evaluation Result")
        st.write(response)
    else:
        st.warning("Please upload a resume and enter the job description.")
