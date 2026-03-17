from parser import extract_text_from_pdf 
from parser import clean_text
import matcher
from rag_utils import split_text_into_chunks
import rag_utils
import parser
import llm_utils

jd_text = """
We are looking for a Python developer with knowledge of SQL, Pandas, NumPy,
Git, Streamlit, and communication skills. Experience in data analysis is a plus.
"""
evaluation_results = []


def process_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    cleanedText = clean_text(text)
    resume_skills = matcher.extract_skills(cleanedText)
    return resume_skills


def process_job_description(jd_text):
    cleanJdText = clean_text(jd_text)
    jd_skills = matcher.extract_skills(cleanJdText)
    return jd_skills

def match_resume_to_jd(pdf_path,jd_text):
    resume_skills = process_resume(pdf_path)
    jd_skills = process_job_description(jd_text)
    if not resume_skills and not jd_skills:
        return {
        "resume_skills": [],
        "jd_skills": [],
        "matched_skills": [],
        "missing_skills": [],
        "score": 0,
        "suggestions": [],
        "message": "No resume skills and no job description skills found."
        }
    if not resume_skills:
         return {
        "resume_skills": [],
        "jd_skills": jd_skills,
        "matched_skills": [],
        "missing_skills": [],
        "score": 0,
        "suggestions": [],
        "message": "No resume text or skills found."
        }
    if not jd_skills:
        return {
        "resume_skills": resume_skills,
        "jd_skills": [],
        "matched_skills": [],
        "missing_skills": [],
        "score": 0,
        "suggestions": [],
        "message": "No JD text or skills found."
        }

    matched_skills, missing_skills = matcher.compare_skill(resume_skill=resume_skills,jd_skill=jd_skills)
    score = matcher.calculate_match_score(matched_skills,jd_skills)
    suggestions = matcher.get_suggestions(missing_skills=missing_skills)

    return {
    "resume_skills": resume_skills,
    "jd_skills": jd_skills,
    "matched_skills": matched_skills,
    "missing_skills": missing_skills,
    "score": score,
    "suggestions": suggestions,
    "message": "Match completed successfully."
}

def display_result(result):
    print(result['message'] )
    print(result['resume_skills'] )
    print(result['jd_skills'] )
    print(result['matched_skills'] )
    print(result['missing_skills'] )
    print(result['score'] )
    
    for suggestion in result['suggestions']:
        print("-",suggestion)



def rag_match_resume_to_jd(pdf_path,jd_text):
   
    parseText = parser.extract_text_from_pdf(pdf_path)
    cleanResumeText = parser.clean_text(parseText)

    chunks = split_text_into_chunks(cleanResumeText)

    jdCleanText = parser.clean_text(jd_text)

    model = rag_utils.load_embedding_model()

    resume_embedding = rag_utils.embed_chunks(chunks,model)
  

    requirements = rag_utils.split_jd_into_requirements(jdCleanText)

    for requirement in requirements:
        query_embedding = rag_utils.embed_chunks([requirement],model)[0]
        top_chunks = rag_utils.retrieve_top_k_chunks(query_embedding,resume_embedding,chunks)
        prompt = rag_utils.build_grounded_prompt(requirement,top_chunks)
        response = llm_utils.analyze_requirement_with_llm(prompt)
        evaluation_results.append({
            "requirement":requirement,
            "top_chunks": top_chunks,
            "prompt":prompt,
            "llm_response": response,
        })
    
    return {
        "requirements_evaluation": evaluation_results,
        "message": "RAG match completed successfully."
    }

print(match_resume_to_jd("./sample_data/dummy_resume.pdf",jd_text))
    
