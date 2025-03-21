import os
import dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables
dotenv.load_dotenv()
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure API key is provided
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is required for this tool.")

# Initialize language model (LLM)
llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

# Initialize embeddings using Hugging Face
embeddings = HuggingFaceEmbeddings()

class VectorDatabase:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.vectorstore = None
    
    def load_documents(self, file_path):
        """ Load and process documents from a text file"""
        
        if not os.path.exists(file_path):
            raise FileExistsError(f" File not found: {file_path}")
        
        # Load documents
        loader= TextLoader(file_path)
        documents = loader.load()
        
        # Splite text into chunks
        text_spliter = CharacterTextSplitter(
            chunk_size= 1000,
            chunk_overlap= 200,
            separator= "\n"
        )
        texts = text_spliter.split_documents(documents)
        
        return texts
    
    def create_vectorstore(self, texts):
        """ Create a vector store from processed documents"""
        
        if not texts:
            raise ValueError(" No text provided to create the vector store.")
        
        self.vectorstore = Chroma.from_documents(
            documents= texts,
            embedding= embeddings,
            persist_directory= self.persist_directory
        )
        self.vectorstore.persist()
        return self.vectorstore
    
    def load_vectorstore(self):
        """ Load an exising vector store from disk """
        
        if not os.path.exists(self.persist_directory):
            raise FileNotFoundError(f" No vector database found at {self.persist_directory} ")

        self.vectorstore = Chroma(
            persist_directory= self.persist_directory,
            embedding_function= embeddings
        )
        return self.vectorstore
    
    def query_database(self, query, k=3):
        """ Query the vector database for relevant documents"""
        
        if not self.vectorstore:
            raise ValueError(" Vector store not initialized. Please create or load a vector store first.")
        
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        qa_chain = RetrievalQA.from_chain_type(
            llm = llm,
            chain_type = "stuff",
            retriever = retriever,
            return_source_documents = True
        )
        
        response = qa_chain.invoke({"query": query})
        return response

# Example usages
db = VectorDatabase()
texts = db.load_documents("documents.txt")
db.create_vectorstore(texts)
db.load_vectorstore()
response = db.query_database("what is the document about?")
print(response)
    