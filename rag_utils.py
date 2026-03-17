from sentence_transformers import SentenceTransformer
import numpy as np

def split_text_into_chunks(text,chunk_size=500,overlap=100):
    if not text:
        return []
    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size")
    
    chunks = []
    start = 0

    while(start < len(text)):
        chunk = text[start:start+chunk_size]
        chunks.append(chunk)
        start += (chunk_size - overlap)

    
    return chunks


def load_embedding_model():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model

def embed_chunks(chunks,model):
    if not chunks:
        return [] 
    
    return model.encode(chunks)


def cosine_similarity(vec1,vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1,vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0

    return dot_product / (norm1 * norm2)

def retrieve_top_k_chunks(query_embedding,chunk_embedding,chunks,top_k = 3):
    scored_chunks = []

    for index, (emb, chunk) in enumerate(zip(chunk_embedding,chunks)):
        score = cosine_similarity(query_embedding,emb)
        scored_chunks.append({
            "chunk_index": index,
            "chunk":chunk,
            "score":score,
        })
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    return scored_chunks[:top_k]

def split_jd_into_requirements(jd_text):
    if not jd_text:
        return []
    
    parts = jd_text.split(".")
    requirements = []

    for part in parts:
        part = part.strip()
        if part and len(part):
            requirements.append(part)
    
    return requirements


def build_grounded_prompt(requirement,top_chunks):
    chunk_text_collector = []

    for chunk in top_chunks:
        chunk_text_collector.append(chunk["chunk"])
    
    evidence_text = "\n\n".join(chunk_text_collector)
    
    prompt = f"""
                    You are evaluating a resume against a job requirement.

                    Requirement:
                    {requirement}

                    Resume Evidence:
                    {evidence_text}

                    Based only on the resume evidence above, decide whether the candidate matches the requirement.

                    Return your answer in this format:
                    Match Status:
                    Explanation:
                    Evidence Used:
                """
    return prompt