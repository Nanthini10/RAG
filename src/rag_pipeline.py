import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

load_dotenv()

class RAGPipeline:
    def __init__(self, model_name="google/flan-t5-small", cache_dir="./models"):
        self.hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_TOKEN not found in .env file")
        
        os.makedirs(cache_dir, exist_ok=True)
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=cache_dir
        )
        
        device = 0 if torch.cuda.is_available() else -1
        
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, 
            token=self.hf_token,
            cache_dir=cache_dir
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name, 
            token=self.hf_token,
            cache_dir=cache_dir
        )
        
        pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            device=device
        )
        
        self.llm = HuggingFacePipeline(pipeline=pipe)
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        
        self.vectorstore = None
    
    def load_documents(self, file_path, use_unstructured=True):
        if use_unstructured and file_path.endswith('.pdf'):
            from langchain_community.document_loaders import UnstructuredPDFLoader
            loader = UnstructuredPDFLoader(
                file_path,
                mode="elements",
                strategy="hi_res",
            )
        elif file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.txt'):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file format. Use .pdf or .txt")
        
        documents = loader.load()
        return self.text_splitter.split_documents(documents)
    
    def create_vectorstore(self, chunks):
        from langchain_community.vectorstores.utils import filter_complex_metadata
        filtered_chunks = filter_complex_metadata(chunks)
        
        self.vectorstore = Chroma.from_documents(
            documents=filtered_chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )
        return self.vectorstore
    
    def summarize_document(self, file_path, chain_type="stuff"):
        chunks = self.load_documents(file_path)
        
        chain = load_summarize_chain(
            self.llm,
            chain_type=chain_type
        )
        
        summary = chain.run(chunks[:5])
        return summary
    
    def query_documents(self, query, k=3):
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Call create_vectorstore first")
        
        results = self.vectorstore.similarity_search(query, k=k)
        return results

if __name__ == "__main__":
    pipeline = RAGPipeline()
    
    # Example usage:
    # summary = pipeline.summarize_document("path/to/document.pdf")
    # print(summary)
