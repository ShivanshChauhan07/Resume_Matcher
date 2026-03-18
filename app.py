import streamlit as st
from service import  match_resume_to_jd
import service
import tempfile

def save_pdf(resume_file):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(resume_file.read())
        return tmp_file.name



st.title("RAG-Based Resume Screening System")

resume_files = st.file_uploader("Upload Resume PDF", type =['pdf'], accept_multiple_files=True)
jd_text = st.text_area("Paste Job Description")

# match_button = st.button("Match Resume")
rag_button = st.button("Rag Match Resume")

# if match_button:
#     if resume_file and jd_text:
#         temp_pdf_path = save_pdf(resume_file)
#         result = match_resume_to_jd(temp_pdf_path,jd_text)

#         st.success(result["message"])
#         st.write(f"Match Score: {result['score']}%")

#         st.subheader("Matched Skills")
#         for skill in result["matched_skills"]:
#             st.write(f"- {skill}")
#         st.subheader("Missing Skills")
#         for skill in result["missing_skills"]:
#             st.write(f"- {skill}")
#         st.subheader("Suggestions")
#         for suggestion in result["suggestions"]:
#             st.write(f"- {suggestion}")
#     else:
#         st.wrtie("Please upload resume and paste job description")

if rag_button:
    if resume_files and jd_text:
        all_results = []

        for resume in resume_files:
            temp_pdf_path = save_pdf(resume)
            result = service.rag_match_resume_to_jd(temp_pdf_path, jd_text)

            all_results.append({
                "filename": resume.name,
                "result": result,
            })

        st.success(f"Processed {len(all_results)} resumes successfully.")

        summary_results = service.build_rag_summary(all_results)

        st.subheader("Resume Ranking Summary")
        for idx, item in enumerate(summary_results, start=1):
            st.write(f"{idx}. {item['filename']}")
            st.write(f"Message: {item['message']}")
            st.write(f"Ranking Score: {item['ranking_score']}")
            st.write(f"Strong Matches: {item['strong_matches']}")
            st.write(f"Partial Matches: {item['partial_matches']}")
            st.write(f"Missing Matches: {item['missing_matches']}")
            if item["unknown_matches"] > 0:
                st.write(f"Unknown Matches: {item['unknown_matches']}")
            st.write("---")

        st.subheader("Detailed RAG Analysis")

        for item in all_results:
            st.markdown(f"## {item['filename']}")
            st.write(item["result"]["message"])

            for eval_item in item["result"]["requirements_evaluation"]:
                st.markdown(f"### Requirement: {eval_item['requirement']}")
                st.write(eval_item["llm_response"])

                st.write("Top Retrieved Resume Chunks:")
                for chunk in eval_item["top_chunks"]:
                    st.write(f"Score: {chunk['score']}")
                    st.write(chunk["chunk"])
                    st.write("---")
    else:
        st.write("Please upload resume files and paste job description.")


