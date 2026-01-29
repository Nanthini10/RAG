RAG Pipeline for Document Summarization

Files:
- src/rag_pipeline.py: Core RAG pipeline with document loading, vectorstore, and summarization
- src/example.py: Example usage demonstrating document summarization and querying
- src/generate_pdfs.py: Generates sample PDF documents for testing
- Dockerfile: Docker image configuration with PyTorch and GPU support
- docker-compose.yml: Docker Compose setup for running container with GPU access
- run_docker.sh: Shell script to build and run Docker container with GPU
- requirements.txt: Python dependencies for the project
- .env.example: Template for environment variables including HuggingFace token
- .gitignore: Git ignore rules for .env, models, cache, and generated files