import streamlit as st
from service import  match_resume_to_jd
import service
import tempfile

def save_pdf(resume_file):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(resume_file.read())
        return tmp_file.name



st.title("Resume + Job Description Matcher")

resume_file = st.file_uploader("Upload Resume PDF", type =['pdf'])
jd_text = st.text_area("Paste Job Description")

match_button = st.button("Match Resume")
rag_button = st.button("Rag Match Resume")

if match_button:
    if resume_file and jd_text:
        temp_pdf_path = save_pdf(resume_file)
        result = match_resume_to_jd(temp_pdf_path,jd_text)

        st.success(result["message"])
        st.write(f"Match Score: {result['score']}%")

        st.subheader("Matched Skills")
        for skill in result["matched_skills"]:
            st.write(f"- {skill}")
        st.subheader("Missing Skills")
        for skill in result["missing_skills"]:
            st.write(f"- {skill}")
        st.subheader("Suggestions")
        for suggestion in result["suggestions"]:
            st.write(f"- {suggestion}")
    else:
        st.wrtie("Please upload resume and paste job description")

if rag_button:
    if resume_file and jd_text:
        temp_pdf_path = save_pdf(resume_file)
        result = service.rag_match_resume_to_jd(temp_pdf_path, jd_text)

        st.success(result["message"])

        for item in result["requirements_evaluation"]:
            st.subheader(item["requirement"])
            st.write(item["llm_response"])

            st.write("Top Retrieved Resume Chunks:")
            for chunk in item["top_chunks"]:
                st.write(f"Score: {chunk['score']}")
                st.write(chunk["chunk"])
                st.write("---")


