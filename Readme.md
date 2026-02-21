AI Resume Screening System

Live App:  
https://ai-resume-screening-s9g859jqbvuufdnzjxpq4t.streamlit.app/

This is a simple AI-powered web app that helps screen and rank resumes against a job description.  
The goal is to simulate how companies do first-level resume filtering before a human recruiter reviews candidates.

I built this project to practice NLP, similarity matching, and deploying a real web application for a practical use case.

-> What this app does

Upload one or multiple resume PDFs  
Paste a job description  
The app reads and cleans the text using NLP  
Ranks each resume based on how relevant it is to the job  
Lets you set a shortlist threshold and see shortlisted candidates  
Works as a web app using Streamlit  

This is useful as a first-pass filter when reviewing many resumes.

->How it works (simple explanation)

1. Text Extraction  
   Reads text from PDF resumes  
   If a resume is scanned, OCR is used (local setup)  

2. Text Cleaning (NLP)  
   Converts text to lowercase  
   Removes noise like emails, symbols, and common filler words  
   Keeps meaningful words such as skills and keywords  

3. Similarity Matching  
   Converts resumes and the job description into vectors using TF-IDF  
   Compares them using cosine similarity  
   Higher score means higher relevance to the job description
   
5. Ranking and Shortlisting  
   Ranks all resumes  
   Shortlists candidates based on a user-defined threshold  

-> Tech Stack
Python  
Streamlit  
NLTK  
scikit-learn  
pdfplumber  
pytesseract and pdf2image (for OCR on local machine)  

-> Run Locally
Bash
pip install -r requirements.txt
streamlit run app.py

Note: For OCR on local machine, make sure Tesseract and Poppler are installed and added to PATH.

