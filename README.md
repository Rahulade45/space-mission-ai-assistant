\# 🚀 Generative AI-Based Space Mission Assistant



An AI-powered Space Mission Assistant that uses \*\*Retrieval-Augmented Generation (RAG)\*\* to provide context-aware answers to space and mission-related questions.



\## 📌 Project Overview



The Generative AI-Based Space Mission Assistant is an interactive application designed to help users explore information related to space missions, satellites, launch vehicles, and space technology.



The system combines document retrieval with a Large Language Model (LLM) to generate relevant and informative responses based on the provided space-related knowledge base.



\## 🎯 Objective



The main objective of this project is to develop an intelligent AI assistant capable of retrieving relevant information from space-mission documents and generating meaningful answers using Generative AI and Retrieval-Augmented Generation.



\## ✨ Key Features



\- 🤖 AI-powered conversational assistant

\- 📚 Retrieval-Augmented Generation (RAG)

\- 🔎 Semantic document search

\- 🛰️ Space mission and space technology information

\- 📄 PDF-based knowledge retrieval

\- 💬 Context-aware question answering

\- 🌐 Interactive Streamlit interface

\- ⚡ LLaMA-based Large Language Model

\- 🔐 Secure API-key management using environment variables



\## 🧠 Methodology



The system follows a Retrieval-Augmented Generation pipeline:



1\. Space-related PDF documents are collected as the knowledge base.

2\. Documents are loaded and processed using LangChain.

3\. Text is divided into smaller chunks.

4\. Text chunks are converted into vector embeddings.

5\. Relevant information is retrieved using semantic similarity.

6\. The retrieved context is provided to the Large Language Model.

7\. The LLM generates a context-aware response.

8\. The response is displayed through the Streamlit interface.



\## 🏗️ System Architecture



```text

Space Mission Documents

&#x20;         │

&#x20;         ▼

&#x20;    PDF Document Loader

&#x20;         │

&#x20;         ▼

&#x20;     Text Processing

&#x20;         │

&#x20;         ▼

&#x20;  Text Chunking / Cleaning

&#x20;         │

&#x20;         ▼

&#x20;  HuggingFace Embeddings

&#x20;         │

&#x20;         ▼

&#x20;    Vector Retrieval

&#x20;         │

&#x20;         ▼

&#x20;  Relevant Context

&#x20;         │

&#x20;         ▼

&#x20;   LLaMA / Groq LLM

&#x20;         │

&#x20;         ▼

&#x20;  Generated Response

&#x20;         │

&#x20;         ▼

&#x20;  Streamlit Web Interface

