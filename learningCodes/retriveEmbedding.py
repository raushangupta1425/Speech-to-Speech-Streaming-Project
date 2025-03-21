# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyMuPDFLoader  # Corrected for PDF support
from langchain.text_splitter import CharacterTextSplitter
from langchain.memory import ConversationBufferMemory
import os
import dotenv

dotenv.load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL") # gemini-1.5-flash
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # A3zaSyA2ljk9PrtRZ-MJswTLFWdbsl5G2O0M7Eo

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

# Get OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API Key is set
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Load PDF document (Fixed TextLoader issue)
pdf_path = "../documents/Artificial_Intelligence.pdf"
loader = PyMuPDFLoader(pdf_path)  # Use PyMuPDFLoader for PDFs
documents = loader.load()

# Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store documents in Chroma vector store
chroma_db = Chroma.from_documents(docs, embeddings)

# Define a retriever
retriever = chroma_db.as_retriever()

# Create a RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

# Define a tool for the agent
tools = [
    Tool(
        name="Chroma DB Retriever",
        func=qa_chain.run,
        description="Use this tool to answer questions based on stored knowledge."
    )
]

# Initialize an agent with memory
memory = ConversationBufferMemory(memory_key="chat_history")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    memory=memory
)

# Query the agent
query = "What does the document say about AI?"
response = agent.run(query)
print(response)
