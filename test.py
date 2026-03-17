from rag_utils import split_text_into_chunks
import rag_utils
import parser
from service import jd_text
import llm_utils

evaluation_results = []


parseText = parser.extract_text_from_pdf("./sample_data/dummy_resume.pdf")
cleanResumeText = parser.clean_text(parseText)

chunks = split_text_into_chunks(cleanResumeText)

jdCleanText = parser.clean_text(jd_text)

jdChunks = split_text_into_chunks(jdCleanText)

model = rag_utils.load_embedding_model()

resume_embedding = rag_utils.embed_chunks(chunks,model)
jd_embedding = rag_utils.embed_chunks(jdChunks,model)

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


print(evaluation_results)