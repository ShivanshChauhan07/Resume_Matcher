from google import genai
from dotenv import load_dotenv

load_dotenv()

def analyze_requirement_with_llm(prompt):
    client = genai.Client()
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text