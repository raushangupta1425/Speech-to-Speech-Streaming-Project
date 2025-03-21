import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader, UnstructuredFileLoader, Docx2txtLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Function to choose appropriate loader based on file extension
def load_all_documents(directory_path):
    loaders = [
        DirectoryLoader(directory_path, glob="*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(directory_path, glob="*.docx", loader_cls=Docx2txtLoader),
        DirectoryLoader(directory_path, glob="*.txt", loader_cls=TextLoader),
        DirectoryLoader(directory_path, glob="*", loader_cls=UnstructuredFileLoader),  # For other file types
    ]

    documents = []
    for loader in loaders:
        documents.extend(loader.load())

    return documents


if __name__ == "__main__":
    
    # 1. Loding Documents
    # print(" Loding Doccument...")
    # loader = TextLoader("../documents/documents.txt")
    # document = loader.load()
    # print(f"Documents Loaded {len(document)}")
    
    # Loading Pdf Documents
    # print(" Loading Pdf Documents...")
    # loader = PyPDFLoader("../documents/Artificial_Intelligence.pdf")
    # document = loader.load()
    # print(f"Documents Loaded {len(document)}")
    
    # Loading Directory documents
    print("Loading Directory documents...")
    directory_path = "../documents"
    document = load_all_documents(directory_path)
    print(f"Documents Loaded: {len(document)}")
    
    #2. Splitting Documents
    print("\nSplitting Documents...")
    splittter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_documents = splittter.split_documents(document)
    print(f"Split {len(document)} documents into {len(split_documents)} chunks.")
    
    #3. Embedding Documents
    print("\nStarted Embedding Documents...")
    embedding = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    print("Embedding Completed")
    
    #4. Inserting Documents intp VectorDB
    print("\nInserting Documents into vectorDB...")
    vector_db = PineconeVectorStore.from_documents(split_documents, embedding, index_name= os.getenv("INDEX_NAME"), pinecone_api_key= os.getenv("PINECONE_API_KEY") )
    print(f"inserted {len(split_documents)} document into vectorDB")