import os
import dotenv
from langchain.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

dotenv.load_dotenv()

GEMINI_MODEL = os.getenv("GEMINI_MODEL") # gemini-1.5-flash
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # A3zaSyA2ljk9PrtRZ-MJswTLFWdbsl5G2O0M7Eo

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

memory= ConversationBufferMemory(memory_key="business_chat_history", return_messages=True)

TEMPLATE = """
You are an AI Business & Entrepreneurship Consultant trained to provide insights into business development and management.

Conversation History:
{business_chat_history}

User: {input}
"""

prompt = PromptTemplate(input_variables=["business_chat_history", "input"], template=TEMPLATE)

conversation = ConversationChain (
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=True,
)

while True:
    user_input = input("User: ")
    
    if user_input.lower() == "exit":
        print("Goodbye! Have a great day!")
        break
    elif user_input.lower() == "reset memory":
        memory.clear()
        print("History cleaned! Start a new conversation.")
        break
    else:
        response = conversation.predict(input= user_input)
        print('AI Chatboat:', response)
        continue
