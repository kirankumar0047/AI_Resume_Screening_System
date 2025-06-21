import streamlit as st
import os
import pandas as pd
from resume_parser import extract_text
from jd_parser import preprocess_jd
from scorer import calculate_similarity

# Ensure clean folder structure
for folder in ["resumes", "jd", "results"]:
    if os.path.isfile(folder):
        os.remove(folder)
    os.makedirs(folder, exist_ok=True)

# Page config
st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("🧠 AI Resume Screener")

# Function to determine match level
def get_match_level(score):
    if score >= 9.0:
        return "🟢 Excellent"
    elif score >= 7.0:
        return "🟡 Good"
    elif score >= 5.0:
        return "🟠 Moderate"
    else:
        return "🔴 Poor"

# JD Upload
st.subheader("📄 Upload JD (.txt file)")
jd_file = st.file_uploader("Upload Job Description", type=["txt"], key="jd_upload")

# Resume Upload
st.subheader("📄 Upload Resume(s)")
resume_files = st.file_uploader(
    "Upload one or more resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True, key="resumes_upload"
)

# Save JD file
jd_path = None
if jd_file:
    jd_path = os.path.join("jd", jd_file.name)
    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())
    st.success(f"✅ JD uploaded: {jd_file.name}")

# Save resumes
resume_paths = []
if resume_files:
    for resume in resume_files:
        save_path = os.path.join("resumes", resume.name)
        with open(save_path, "wb") as f:
            f.write(resume.getbuffer())
        resume_paths.append(save_path)
    st.success(f"✅ {len(resume_paths)} resume(s) uploaded")

# Matching logic
if st.button("🧠 Match Resumes with JD"):
    if not jd_file or not resume_paths:
        st.warning("⚠️ Please upload both job description and at least one resume.")
    else:
        jd_text = open(jd_path, "r", encoding="utf-8").read()
        processed_jd = preprocess_jd(jd_text)

        results = []
        for resume_path in resume_paths:
            resume_text = extract_text(resume_path)
            if not resume_text:
                st.error(f"❌ Could not extract: {os.path.basename(resume_path)}")
                continue

            score = calculate_similarity(resume_text, processed_jd)
            match_level = get_match_level(score)

            results.append({
                "Resume": os.path.basename(resume_path),
                "Match Score (out of 10)": score,
                "Match Level": match_level
            })

        if results:
            df = pd.DataFrame(results).sort_values(by="Match Score (out of 10)", ascending=False)
            st.dataframe(df, use_container_width=True)

            # 📊 Graph: Bar chart of scores
            st.subheader("📊 Resume Match Scores (Out of 10)")
            st.bar_chart(df.set_index("Resume")["Match Score (out of 10)"])

            # 📊 Graph: Match Level Distribution
            st.subheader("📊 Match Level Distribution")
            level_counts = df["Match Level"].value_counts()
            st.bar_chart(level_counts)

            # Save results
            result_path = os.path.join("results", "match_results.csv")
            df.to_csv(result_path, index=False)
            st.download_button("📥 Download Results CSV", data=df.to_csv(index=False), file_name="match_results.csv", mime="text/csv")
        else:
            st.error("❌ No valid resumes processed.")