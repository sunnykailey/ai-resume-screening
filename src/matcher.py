from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(cleaned_resumes, cleaned_jd):
    documents = cleaned_resumes + [cleaned_jd]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    jd_vector = tfidf_matrix[-1]
    resume_vectors = tfidf_matrix[:-1]

    scores = cosine_similarity(resume_vectors, jd_vector)

    return scores.flatten()
