from rank_bm25 import BM25Okapi

def hybrid_search(question,vectorstore,documents):

    vector_results = vectorstore.similarity_search(question,k=5)
    
    corpus = [doc.split() for doc in documents]

    bm25 = BM25Okapi(corpus)
    scores = bm25.get_scores(question.split())

    return vector_results