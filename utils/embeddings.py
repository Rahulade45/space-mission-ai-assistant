from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore")


def create_vectorstore(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        docs,
        embeddings
    )

    os.makedirs(VECTORSTORE_PATH, exist_ok=True)

    vectorstore.save_local(VECTORSTORE_PATH)

    return vectorstore


def load_vectorstore():

    index_file = os.path.join(VECTORSTORE_PATH, "index.faiss")
    pickle_file = os.path.join(VECTORSTORE_PATH, "index.pkl")

    # Vector database does not exist yet
    if not os.path.isfile(index_file) or not os.path.isfile(pickle_file):
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )