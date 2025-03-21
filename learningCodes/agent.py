import os
import dotenv
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
# from langchain.llms import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory

dotenv.load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL") # gemini-1.5-flash
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # A3zaSyA2ljk9PrtRZ-MJswTLFWdbsl5G2O0M7Eo

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

# Set OpenAI API Key
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"  # Replace with your actual API key

# # Define the LLM (Language Model)
# llm = OpenAI(model_name="gpt-4", temperature=0)

# Define a simple calculator tool
def calculator_tool(query: str):
    try:
        return eval(query)
    except:
        return "Invalid math expression."

calc_tool = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Use this tool to solve math expressions."
)

# Define Memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the Agent
agent = initialize_agent(
    tools=[calc_tool],  # Add more tools as needed
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Type of agent
    memory=memory,
    verbose=True
)

# Run the chatbot loop
print("Chatbot is running! Type 'exit' to stop.")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Goodbye!")
        break
    response = agent.run(user_input)
    print("Chatbot:", response)
