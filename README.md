# 🧠 AI-Powered Document Assistant

This project is a **Retrieval-Augmented Generation (RAG)** application built using Python and Streamlit. It allows users to upload `.txt` or `.pdf` documents, extract their content, embed it, and use the **OpenAI GPT model** to answer questions based on the content of the uploaded document.

---

## 📆 Project Structure

```
ai_document_reader/
├── sample_docs/                 # Example documents for testing
│   ├── sample1.txt
│   ├── sample2.txt
│   └── sample.pdf
├── .env                         # API key and model name (excluded in submission)
├── .streamlit/                  # Streamlit configuration
├── app.py                       # Main Streamlit app
├── rag_engine.py                # Chunking, embedding, and answer generation
├── utils.py                     # File extraction utilities
├── requirements.txt             # Required Python packages
├── README.md                    # Instructions and project details
└── example_qna.txt              # Sample questions & answers
```

---

## 🛠️ Setup Instructions

### 1. Extract the zip file

Open the project in IDE and open the terminal.

---

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# OR on Windows
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add your key to `.env` file

Replace with your API_KEY:

```
OPENAI_API_KEY="your-openai-key-here"
OPEN_AI_MODEL="gpt-3.5-turbo"
```

---

### 5. Run the application

```bash
streamlit run app.py
```

Open the link shown in your terminal (usually `http://localhost:8501`) to use the app.

---

## 📚 Technologies Used

- Python 3.11+
- Streamlit
- OpenAI GPT-3.5 Turbo
- `python-dotenv` for environment variable handling
- `pdfplumber` for PDF text extraction
- `numpy` for vector math and similarity scoring

---

## ✨ What This App Can Do

- Upload multiple `.txt` or `.pdf` documents
- Automatically split and embed document text
- Ask natural language questions across all documents
- Retrieve relevant chunks based on cosine similarity
- Generate contextual answers using OpenAI GPT-3.5 Turbo
- Show citations (chunk and document) used to answer
- Gracefully respond when info is not found
- Includes a clean and styled Streamlit interface with dark mode

---

## 💻 Developed by

**Ana Abashidze**  
**Otari Abashidze**  
**Zezva Kobaidze**

Kutaisi International University  
AI-Powered Applications – Spring 2025