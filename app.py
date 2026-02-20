import streamlit as st
import os
import tempfile

from src.preprocess import clean_text
from src.matcher import rank_resumes
from main import extract_text_from_pdf  # reuse your function

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("🧠 AI Resume Screening System")
st.caption("Upload resumes + paste a Job Description to rank candidates")

# Upload resumes
uploaded_files = st.file_uploader(
    "Upload resume PDFs (multiple allowed)",
    type=["pdf"],
    accept_multiple_files=True
)

# Job Description input
jd_text = st.text_area("Paste Job Description here", height=150)

threshold = st.slider("Shortlist threshold (%)", min_value=5, max_value=50, value=15)

if st.button("🔍 Rank Resumes"):

    if not uploaded_files or not jd_text.strip():
        st.warning("Please upload at least one resume and add a Job Description.")
    else:
        all_cleaned_resumes = []
        resume_names = []

        with st.spinner("Processing resumes..."):
            for file in uploaded_files:
                # Save temp PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                text = extract_text_from_pdf(tmp_path)
                cleaned = clean_text(text)

                all_cleaned_resumes.append(cleaned)
                resume_names.append(file.name)

                os.remove(tmp_path)

        cleaned_jd = clean_text(jd_text)
        scores = rank_resumes(all_cleaned_resumes, cleaned_jd)

        st.subheader("📊 Resume Match Scores")
        results = sorted(zip(resume_names, scores), key=lambda x: x[1], reverse=True)

        for name, score in results:
            st.write(f"**{name}** → {score*100:.1f}%")

        st.subheader("✅ Shortlisted Candidates")
        shortlisted = [(n, s) for n, s in results if s*100 >= threshold]

        if shortlisted:
            for name, score in shortlisted:
                st.success(f"{name} → {score*100:.1f}%")
        else:
            st.info("No candidates met the shortlist threshold.")
