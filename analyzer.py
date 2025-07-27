from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections(sections, persona, job_to_be_done):
    query = f"{persona}: {job_to_be_done}"
    texts = [s["content"] for s in sections]

    vectorizer = TfidfVectorizer().fit([query] + texts)
    vectors = vectorizer.transform([query] + texts)

    scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    ranked = sorted(zip(sections, scores), key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked]

def refine_subsections(sections, persona, job_to_be_done):
    keywords = job_to_be_done.lower().split()
    refined = []

    for sec in sections:
        lines = sec["content"].split(". ")
        best_lines = [line for line in lines if any(k in line.lower() for k in keywords)]

        summary = ". ".join(best_lines[:2]).strip()
        if summary:
            refined.append({
                "document": sec["document"],
                "section_title": sec["section_title"],
                "refined_text": summary,
                "page_number": sec.get("page_number", -1)
            })

    return refined
