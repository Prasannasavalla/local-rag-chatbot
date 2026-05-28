import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

st.set_page_config(page_title="Local Legal & Ethics AI", layout="wide")
st.title("⚖️ Private RAG Legal & Ethics Expert Chatbot")
st.markdown("Ask questions about your uploaded PDF. Everything is processed 100% locally on your machine.")

PDF_PATH = "document.pdf"

# --- 1. PROCESSS & VECTORIZE PDF (Cached so it runs once) ---
@st.cache_resource
def initialize_vector_db():
    if not os.path.exists(PDF_PATH):
        return None
        
    # Load the PDF file
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    
    # Split text into small paragraphs (chunks)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    
    # Convert text chunks into math vector numbers using a free open-source model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Store vectors in a temporary local database
    vector_db = Chroma.from_documents(chunks, embeddings)
    return vector_db

# Initialize database
with st.spinner("Reading PDF and initializing local AI vector database..."):
    db = initialize_vector_db()

# --- 2. CHAT INTERFACE & INFERENCE ---
if db is None:
    st.error(f"Please place your file named '{PDF_PATH}' inside the project folder and refresh the page!")
else:
    st.success("✅ Document vectorized! Your local LLM is ready to answer questions.")
    
    # Initialize chat history state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user question input
    if user_query := st.chat_input("Ask me anything about the document..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # RAG Logic: Search database for the top 3 most relevant paragraphs
        with st.chat_message("assistant"):
            with st.spinner("Searching document data layers..."):
                relevant_docs = db.similarity_search(user_query, k=3)
                context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
                
                # Construct a strict prompt telling the LLM to only use the document text
                system_prompt = f"""You are an expert legal and ethics assistant. 
Answer the user's question using ONLY the provided document context below. 
If the answer cannot be found in the context, say 'I cannot find that information in the uploaded document.'

CONTEXT:
{context_text}

QUESTION:
{user_query}
"""
                # Stream the response back from the local Ollama model
                llm = Ollama(model="qwen2.5:0.5b")
                response_placeholder = st.empty()
                full_response = ""
                
                # Run local inference chunk by chunk
                for chunk in llm.stream(system_prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")
                
                response_placeholder.markdown(full_response)
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})