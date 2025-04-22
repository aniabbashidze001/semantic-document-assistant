from rag_engine import process_document_for_retrieval, retrieve_top_chunks, generate_answer
from utils import extract_text_from_pdf, extract_text_from_txt
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()
MODEL_NAME = os.getenv("OPEN_AI_MODEL")

st.set_page_config(page_title="Semantic Search Engine", layout="centered")

st.markdown("# 📄 Semantic Document Search Engine")
st.markdown("Upload multiple documents and ask questions to get AI-powered, source-aware answers.")

# Init embedded_chunks if not present
if "embedded_chunks" not in st.session_state:
    st.session_state["embedded_chunks"] = []

# Sidebar reset option
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🔄 Clear Session"):
        st.session_state.clear()
        st.success("Session cleared. Please refresh manually to reset UI.")

# Upload section
st.subheader("📂 Upload Your Documents")
uploaded_files = st.file_uploader("Choose one or more files", type=["pdf", "txt"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name
        file_type = uploaded_file.type

        if file_type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif file_type == "text/plain":
            document_text = extract_text_from_txt(uploaded_file)
        else:
            continue

        st.markdown(f"**✅ Extracted from `{file_name}`**")
        st.text_area("Document Preview", document_text[:2000], height=200)

        with st.spinner(f"🔄 Processing `{file_name}`..."):
            embedded = process_document_for_retrieval(document_text, doc_name=file_name)
            st.session_state.embedded_chunks.extend(embedded)

    st.success(f"✅ {len(uploaded_files)} file(s) processed into {len(st.session_state.embedded_chunks)} total chunks.")

# Ask questions
if st.session_state.embedded_chunks:
    st.markdown("---")
    st.subheader("💬 Ask Your Question")

    user_question = st.text_input("What do you want to know?", placeholder="e.g. What are the four forces of flight?")

    if user_question:
        with st.spinner("🔍 Searching and generating answer..."):
            top_chunks = retrieve_top_chunks(user_question, st.session_state.embedded_chunks, threshold=0.7)

            if not top_chunks:
                st.warning("🤔 No relevant information found across uploaded documents.")
            else:
                try:
                    answer = generate_answer(user_question, top_chunks)
                except Exception as e:
                    st.error("❌ Failed to generate answer.")
                    st.exception(e)
                    answer = None

                if answer:
                    st.markdown("#### 🧠 Assistant")
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f2f6; padding: 12px 18px; border-radius: 12px; color:#000000;
                        border-left: 4px solid #4A90E2; margin-top: 10px;">
                        {answer.strip()}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Show citations only if answer isn't a fallback
                    if "i couldn't find that in the documents" not in answer.lower():
                        with st.expander("📚 View Citations (Sources Used)"):
                            for i, chunk in enumerate(top_chunks):
                                doc_name = chunk.get("doc_name", "Unknown")
                                st.markdown(f"**Chunk {i + 1} — from `{doc_name}`:**")
                                st.code(chunk["chunk"][:800], language="text")
                    else:
                        st.info("No citations shown because no document information matched the question.")
