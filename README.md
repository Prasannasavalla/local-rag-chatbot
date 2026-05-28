# Private RAG Legal & Ethics Expert Chatbot ⚖️🤖

### Purpose of the Project
When dealing with sensitive legal documents or dense educational textbooks, uploading files to public cloud AI platforms can risk data privacy. The aim of this project is to build a completely private, offline Retrieval-Augmented Generation (RAG) system. It reads complex PDF documents, processes them into mathematical structures locally, and uses a lightweight open-source Large Language Model (LLM) to answer domain-specific questions without any data leaving your machine.

---

##  The Tech Stack

* **LLM Core Platform:** Ollama (`qwen2.5:0.5b` optimized quantized engine)
* **Application Framework:** LangChain (Document loaders, text splitters, and prompt chains)
* **Vector Database Engine:** ChromaDB
* **Text Embeddings Neural Network:** HuggingFace (`all-MiniLM-L6-v2`)
* **User Interface Layout:** Streamlit
* **Core Language:** Python 3.10

---

##  Features

* **(1)100% Offline Processing:** Runs completely isolated from the internet—no cloud subscriptions or API keys needed.
* **(2)Semantic Vector Searching:** Chops long books into distinct paragraphs, converts them into embeddings, and queries them instantly using vector calculations.
* **(3)Streamed Responses:** Generates context-bounded answers word-by-word directly on your local CPU/GPU hardware.


---

##  Future Enhancements

To scale this local prototype for institutional use, the following enhancements are planned:

* **Hybrid Search Retrieval:** Merge keyword matching (BM25) with semantic vector search to improve the retrieval accuracy of specific legal sub-clauses.
* **Source Attribution UI:** Modify the Streamlit application interface to highlight the exact page numbers and chapter headers where the AI found its source material.
* **Multi-Format Processing:** Extend the document loading system to support cross-referencing markdown files, raw text files, and docx tables simultaneously.
##  How to Clone & Run

You can spin up this private legal chatbot locally on your machine by running these steps in your terminal:

```bash
# 1. Clone the project and navigate into the folder
git clone [https://github.com/prasannasavalla/local-rag-chatbot.git](https://github.com/prasannasavalla/local-rag-chatbot.git)
cd local-rag-chatbot

# 2. Set up and activate a clean Python virtual environment
python -m venv venv
# On Windows Command Prompt:
venv\Scripts\activate.bat
# On macOS / Linux: source venv/bin/activate

# 3. Install the required Generative AI packages
pip install -r requirements.txt

# 4. Make sure Ollama is running in the background and pull the model
ollama run qwen2.5:0.5b

# 5. Launch the local web interface!
streamlit run app.py
