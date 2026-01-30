import streamlit as st
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag_pipeline import RAGPipeline

st.set_page_config(page_title="RAG Document Q&A", layout="wide")

@st.cache_resource
def load_pipeline():
    return RAGPipeline(model_name="google/flan-t5-small")

def save_uploaded_file(uploaded_file):
    temp_dir = Path("uploaded_docs")
    temp_dir.mkdir(exist_ok=True)
    file_path = temp_dir / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)

st.title("RAG Document Q&A System")

pipeline = load_pipeline()

if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                all_chunks = []
                for uploaded_file in uploaded_files:
                    file_path = save_uploaded_file(uploaded_file)
                    st.info(f"Processing {uploaded_file.name}...")
                    chunks = pipeline.load_documents(file_path)
                    all_chunks.extend(chunks)
                    st.session_state.processed_files.append(uploaded_file.name)
                
                pipeline.create_vectorstore(all_chunks)
                st.session_state.vectorstore_ready = True
                st.success(f"Processed {len(uploaded_files)} documents!")
        else:
            st.warning("Please upload at least one document")
    
    if st.session_state.processed_files:
        st.subheader("Processed Documents")
        for filename in st.session_state.processed_files:
            st.text(f"✓ {filename}")
    
    if st.button("Clear All"):
        st.session_state.vectorstore_ready = False
        st.session_state.processed_files = []
        st.session_state.chat_history = []
        pipeline.vectorstore = None
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Ask Questions")
    
    if st.session_state.vectorstore_ready:
        query = st.text_input("Enter your question:", key="query_input")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            search_button = st.button("Search", type="primary")
        with col_btn2:
            num_results = st.slider("Results", 1, 10, 3, key="num_results")
        
        if search_button and query:
            with st.spinner("Searching..."):
                results = pipeline.query_documents(query, k=num_results)
                st.session_state.chat_history.append({
                    "query": query,
                    "results": results
                })
        
        if st.session_state.chat_history:
            st.subheader("Query Results")
            for idx, item in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {item['query']}", expanded=(idx==0)):
                    for i, doc in enumerate(item['results']):
                        st.markdown(f"**Result {i+1}** (Source: {doc.metadata.get('source', 'Unknown')})")
                        st.text_area(
                            f"Content {i+1}",
                            doc.page_content,
                            height=150,
                            key=f"result_{idx}_{i}",
                            label_visibility="collapsed"
                        )
                        st.divider()
    else:
        st.info("Please upload and process documents first using the sidebar.")

with col2:
    st.header("Summarization")
    
    if st.session_state.vectorstore_ready and st.session_state.processed_files:
        selected_doc = st.selectbox(
            "Select document to summarize",
            st.session_state.processed_files
        )
        
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                doc_path = f"uploaded_docs/{selected_doc}"
                summary = pipeline.summarize_document(doc_path)
                st.subheader("Summary")
                st.write(summary)
    else:
        st.info("Process documents to enable summarization")
