import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import getpass
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

# Load environment variables
load_dotenv()

## Embedding technique of OpenAI
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Pinecone
if not os.getenv("PINECONE_API_KEY"):
    os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")
pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])

index_name = os.getenv("INDEX_NAME")  # change if desired

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
if index_name not in existing_indexes:
    print("Creating index first...")
index = pc.Index(index_name)  # Connect to the existing index

# Load the existing index into LangChain's Pinecone wrapper
vectorstore = PineconeVectorStore(index, embedding=embeddings)

# Initialize language model (LLM)
llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL"), temperature=0.7)

# Retrieve data from the Pinecone database index
def retrieve_pinecone_data():
    retriever = vectorstore.as_retriever()
    return retriever

# Create a chain of functions
def chain_fun(retriever, llm):
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt
    )
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)
    return retrieval_chain

# Search for the answer
def retrieve_answer(query, llm):
    db_retrieve_data = retrieve_pinecone_data()
    chain= chain_fun(db_retrieve_data, llm)
    response = chain.invoke({"input": query})
    return response

# Ask a question
our_query = input("Enter your query: ")
answer = retrieve_answer(our_query, llm)
print(answer)

