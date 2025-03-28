import os
import dotenv
from langchain.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI

class TranslateText:
    def translate_text(self, user_input, target_language):
        print("Translating the text...")
        dotenv.load_dotenv()

        GEMINI_MODEL = os.getenv("GEMINI_MODEL") # gemini-1.5-flash
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Need to load GOOGLE_API_KEY from environment.

        llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.7)

        TEMPLATE = f"""
        You are an Languages Translator Assistant trained to provide accurate translation of the user inputs. You will:
        1. Translate the user's input by analyzing the language code. 
        2. Read the user's text, analyze the text source language and translate the user's text into target language code ${target_language}.
        2. Do not add any word and sentences extra.
        3. Must generate meaning sentences with proper punctuation marks.

        You are only allowed to translate the user's input to the targeted language.

        IMPORTANT: I am an AI assistant and trained for translate the user's input to the targeted language only cannot provide any other details.

        ${user_input}
        """

        prompt = PromptTemplate.from_template(TEMPLATE)

        chain = prompt | llm

        response = chain.invoke({"input": user_input})
        print("Translated Text successfully!")

        return response.content
