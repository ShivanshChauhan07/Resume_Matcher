
skill_list = ["python", "sql", "excel", "streamlit", "pandas", "numpy", "git"]

def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    found_list = []

    for skill in skill_list:
        if skill in text:
            found_list.append(skill)
    
    return sorted(set(found_list)) 

def compare_skill(resume_skill,jd_skill):
    matched_skill = []
    missing_skill = []

    for skill in jd_skill:
        if skill in resume_skill:
            matched_skill.append(skill)
        else:
            missing_skill.append(skill)
        
    return matched_skill,missing_skill

def calculate_match_score(matched_skills,jd_skills):
    totalScore = len(jd_skills)
    score = 0
    if totalScore == 0:
        return 0
    for skill in jd_skills:
        if skill in matched_skills:
            score += 1
    
    finalScore = (score / totalScore) * 100

    return round(finalScore,2)

def get_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        msg = f"Try adding {skill} to your resume if you have worked on it."
        suggestions.append(msg)
    

    return suggestions
