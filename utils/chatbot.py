from langchain_groq import ChatGroq
from utils.prompt import SYSTEM_PROMPT


def ask_question(vectorstore, question, api_key):

    docs = vectorstore.similarity_search(
        question,
        k=4
    )

    context = ""

    for doc in docs:
        context += doc.page_content + "\n\n"

    llm = ChatGroq(
        api_key=api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)

    return response.content