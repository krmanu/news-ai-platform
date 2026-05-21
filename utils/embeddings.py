from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_embeddings():
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings

def create_vectorstore(documents):
    embeddings = load_embeddings()
    vectorstore = FAISS.from_texts(documents,embedding=embeddings)
    return vectorstore
