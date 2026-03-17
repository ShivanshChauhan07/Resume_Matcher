import pdfplumber

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        resume_text = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text.append(text)

    if not resume_text:
        return ''
    
    finalText = "\n".join(resume_text)

    return finalText


def clean_text(text):
    words = text.strip().split()
    cleaned = " ".join(words)
    return cleaned





    
