import os
import shutil
from dotenv import load_dotenv
import streamlit as st

from utils.loader import load_documents
from utils.embeddings import create_vectorstore, load_vectorstore
from utils.chatbot import ask_question


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Space Mission AI Assistant",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# API KEY CHECK
# ============================================================

if not GROQ_API_KEY:
    st.error(
        "❌ GROQ_API_KEY not found.\n\n"
        "Please create a .env file in the project folder and add:\n\n"
        "GROQ_API_KEY=your_groq_api_key"
    )
    st.stop()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
    }

    .subtitle {
        font-size: 18px;
        color: #666;
    }

    .success-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #e8f8ee;
        border: 1px solid #b7e4c7;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.image(
        "images/rocket.png",
        width=120
    )

    st.title("Space Mission AI")

    st.divider()

    st.subheader("📚 Knowledge Base")

    st.write(
        "This chatbot can answer questions from:"
    )

    st.write("✅ ISRO")
    st.write("✅ NASA")
    st.write("✅ Chandrayaan-3")
    st.write("✅ Gaganyaan")
    st.write("✅ Aditya-L1")
    st.write("✅ Mars")
    st.write("✅ Moon")
    st.write("✅ Space Exploration")

    st.divider()

    st.subheader("🛠️ Technologies")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• LangChain")
    st.write("• FAISS")
    st.write("• HuggingFace")
    st.write("• Groq LLM")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ============================================================
# MAIN TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🚀 Space Mission AI Assistant</div>',
    unsafe_allow_html=True
)

st.write(
    "Generative AI-powered Space Mission Assistant using "
    "Retrieval-Augmented Generation (RAG)."
)

st.success(
    "🚀 Welcome Rahul! Ready to explore Space."
)


# ============================================================
# INFORMATION
# ============================================================

st.subheader("Ask questions about:")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("🛰️ Chandrayaan Missions")
    st.write("👨‍🚀 Gaganyaan")
    st.write("🇮🇳 ISRO")

with col2:
    st.write("🌎 NASA")
    st.write("☀️ Aditya-L1")
    st.write("🔴 Mars")

with col3:
    st.write("🌙 Moon")
    st.write("🚀 Space Exploration")
    st.write("🛸 Space Technology")


# ============================================================
# VECTORSTORE FUNCTION
# ============================================================

def build_knowledge_base():

    with st.spinner(
        "🔄 Creating knowledge base from space documents..."
    ):

        docs = load_documents("data")

        if not docs:
            st.error(
                "❌ No PDF documents found in the data folder."
            )
            return None

        vectorstore = create_vectorstore(docs)

        return vectorstore


# ============================================================
# LOAD EXISTING VECTORSTORE
# ============================================================

vectorstore = load_vectorstore()


# ============================================================
# CREATE VECTORSTORE IF NOT AVAILABLE
# ============================================================

if vectorstore is None:

    vectorstore = build_knowledge_base()

    if vectorstore is None:
        st.stop()


# ============================================================
# QUESTION SECTION
# ============================================================

st.divider()

st.subheader("💬 Ask Your Space Question")

question = st.text_input(
    "Ask your Space Question",
    placeholder="Example: Explain Chandrayaan-3 Mission"
)


# ============================================================
# ANSWER QUESTION
# ============================================================

if question:

    with st.spinner("🤖 Searching the knowledge base..."):

        try:

            answer = ask_question(
                question,
                vectorstore,
                GROQ_API_KEY
            )

            st.subheader("🤖 Answer")

            st.write(answer)

        except Exception as e:

            error_message = str(e)

            if "401" in error_message or "Invalid API Key" in error_message:

                st.error(
                    "❌ Invalid Groq API key.\n\n"
                    "Please generate a new Groq API key and "
                    "update your .env file."
                )

            else:

                st.error(
                    f"❌ Error while generating answer:\n\n{e}"
                )


# ============================================================
# PDF UPLOAD
# ============================================================

st.divider()

st.subheader("📄 Upload Space PDF")

st.write(
    "Upload one or more space-related PDF documents. "
    "The knowledge base will automatically rebuild."
)

uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True
)


# ============================================================
# HANDLE PDF UPLOAD
# ============================================================

if uploaded_files:

    os.makedirs("data", exist_ok=True)

    uploaded_any = False

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            "data",
            uploaded_file.name
        )

        try:

            with open(file_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            uploaded_any = True

        except Exception as e:

            st.error(
                f"❌ Could not save {uploaded_file.name}: {e}"
            )


    if uploaded_any:

        st.success(
            "✅ PDF uploaded successfully!"
        )

        # ----------------------------------------------------
        # DELETE OLD VECTORSTORE
        # ----------------------------------------------------

        if os.path.exists("vectorstore"):

            try:

                shutil.rmtree("vectorstore")

            except Exception as e:

                st.error(
                    f"❌ Could not remove old vectorstore: {e}"
                )
                st.stop()


        # ----------------------------------------------------
        # REBUILD VECTORSTORE
        # ----------------------------------------------------

        with st.spinner(
            "🔄 Processing PDFs and rebuilding knowledge base..."
        ):

            try:

                docs = load_documents("data")

                vectorstore = create_vectorstore(docs)

                st.success(
                    "✅ Knowledge base rebuilt successfully!"
                )

                st.info(
                    "🚀 Your newly uploaded PDF is now available "
                    "for questions."
                )

            except Exception as e:

                st.error(
                    f"❌ Failed to rebuild knowledge base:\n\n{e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🚀 Space Mission AI Assistant | "
    "Powered by LangChain + FAISS + HuggingFace + Groq"
)