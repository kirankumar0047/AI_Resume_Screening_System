# main.py

import os
from resume_parser import extract_text
from jd_parser import preprocess_jd
from scorer import calculate_similarity

# === Input File Paths ===
resume_file = os.path.join("resumes", "sample_resume.pdf")  # You can change this to .docx or .txt
jd_file = os.path.join("jd", "jd_text.txt")                 # ✅ Job description from .txt file

# === Step 1: Extract Resume Text ===
if os.path.exists(resume_file):
    resume_text = extract_text(resume_file)
else:
    print("❌ Resume file not found:", resume_file)
    exit()

# === Step 2: Read and Preprocess Job Description ===
if os.path.exists(jd_file):
    with open(jd_file, 'r', encoding='utf-8') as f:
        job_description_text = f.read()
else:
    print("❌ Job description file not found:", jd_file)
    exit()

processed_jd = preprocess_jd(job_description_text)

# === Step 3: Calculate Similarity Score ===
score = calculate_similarity(resume_text, processed_jd)

# === Step 4: Output ===
print("\n📄 Resume File:", os.path.basename(resume_file))
print("📄 JD File:", os.path.basename(jd_file))
print(f"✅ Match Score: {score}%\n")