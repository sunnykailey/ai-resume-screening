import pdfplumber
import os
import pytesseract
from pdf2image import convert_from_path
from src.preprocess import clean_text
from src.matcher import rank_resumes

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

resume_folder = "data/resumes"

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    if len(text.strip()) == 0:
        print("⚠ No text found, using OCR...")
        images = convert_from_path(file_path)  
        for img in images:
            text += pytesseract.image_to_string(img)

    return text
all_cleaned_resumes = []
resume_names = []

for file in os.listdir(resume_folder):
    if file.endswith(".pdf"):
        file_path = os.path.join(resume_folder, file)
        print(f"\nReading: {file}")

        text = extract_text_from_pdf(file_path)

        print("----- Extracted Text (first 200 chars) -----")
        print(text[:200])

        cleaned = clean_text(text)
        print("----- CLEANED TEXT (first 200 chars) -----")
        print(cleaned[:200])

        all_cleaned_resumes.append(cleaned)
        resume_names.append(file)
        with open("data/job_description.txt", "r", encoding="utf-8") as f:
            jd_text = f.read()
            cleaned_jd = clean_text(jd_text)
            scores = rank_resumes(all_cleaned_resumes, cleaned_jd)
            print("\n📊 Resume Match Scores:")
            for name, score in sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True):
                print(f"{name}  ->  Match: {score*100:.1f}%")
                threshold = 0.15
                print("\n✅ Shortlisted Candidates:")
                for name, score in sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True):
                    if score >= threshold:
                        print(f"{name}  ->  {score*100:.1f}%")