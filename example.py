from rag_pipeline import RAGPipeline

pipeline = RAGPipeline(model_name="google/flan-t5-small")

doc_path = "data/healthcare_ml.pdf"
summary = pipeline.summarize_document(doc_path)
print("Summary:", summary)

chunks = pipeline.load_documents(doc_path)
pipeline.create_vectorstore(chunks)

query = "What are the main points?"
results = pipeline.query_documents(query, k=3)
for i, doc in enumerate(results):
    print(f"\nResult {i+1}:", doc.page_content[:200])
