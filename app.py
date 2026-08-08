import streamlit as st
import os
from dotenv import load_dotenv

from utils.loader import load_documents
from utils.embeddings import create_vectorstore, load_vectorstore
from utils.chatbot import ask_question
from utils.helper import welcome, footer

# ----------------------------
# Load API Key
# ----------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="🚀 Space Mission AI Assistant",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:

    st.image("images/rocket.png", width=120)

    st.title("Space Mission AI")

    st.markdown("---")

    st.subheader("📚 Knowledge Base")

    st.write("This chatbot can answer questions from:")

    st.markdown("""
✅ ISRO

✅ NASA

✅ Chandrayaan-3

✅ Gaganyaan

✅ Aditya-L1
""")

    st.markdown("---")

    st.subheader("🛰 Technologies")

    st.markdown("""
- Python
- Streamlit
- LangChain
- FAISS
- HuggingFace
- Groq LLM
""")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# Main Page
# ----------------------------

st.title("🚀 Space Mission AI Assistant")

welcome()

st.write(
    """
Ask questions about:

- Chandrayaan Missions
- Gaganyaan
- ISRO
- NASA
- Aditya-L1
- Mars
- Moon
- Space Exploration
"""
)

# ----------------------------
# Load Vector Database
# ----------------------------

vectorstore = load_vectorstore()

if vectorstore is None:

    with st.spinner("Creating Knowledge Base..."):

        docs = load_documents("data")

        vectorstore = create_vectorstore(docs)

# ----------------------------
# Question Box
# ----------------------------

question = st.text_input(
    "Ask your Space Question",
    placeholder="Example: Explain Chandrayaan-3 Mission"
)

if st.button("🚀 Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        answer = ask_question(
            vectorstore,
            question,
            GROQ_API_KEY
        )

        st.session_state.messages.append(
            {
                "question": question,
                "answer": answer
            }
        )
        # ----------------------------
# Chat History
# ----------------------------

if len(st.session_state.messages) > 0:

    st.markdown("---")

    st.header("💬 Conversation")

    for chat in reversed(st.session_state.messages):

        st.markdown(
            f"""
### 🙋 Question

{chat['question']}

### 🤖 Answer

{chat['answer']}

---
"""
        )

footer()
import os

st.subheader("📄 Upload Space PDF")

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    os.makedirs("data", exist_ok=True)

    for file in uploaded_files:
        with open(os.path.join("data", file.name), "wb") as f:
            f.write(file.getbuffer())

    st.success("✅ PDF uploaded successfully!")

    st.info("Please restart the app or rebuild the vector database to include the new PDFs.")