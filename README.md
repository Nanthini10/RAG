RAG Pipeline for Document Summarization

## Directory Structure
```
RAG/
├── src/
│   ├── app.py              # Streamlit web interface
│   ├── rag_pipeline.py     # Core RAG pipeline
│   └── generate_pdfs.py    # PDF generation utility
├── scripts/
│   ├── example.py          # CLI example usage
│   └── run_docker.sh       # Docker run script
├── data/                   # Sample PDFs
├── uploaded_docs/          # User-uploaded PDFs (auto-created)
├── models/                 # Cached models (auto-created)
├── chroma_db/              # Vector database (auto-created)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Setup
```bash
sudo docker-compose build
sudo docker-compose up -d
sudo docker-compose exec rag-dev bash
```

## Run Streamlit App
```bash
streamlit run src/app.py --server.address=0.0.0.0
```
Access at: http://localhost:8501

## Run CLI Example
```bash
python scripts/example.py
```