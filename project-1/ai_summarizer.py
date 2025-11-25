from langchain.chat_models import init_chat_model
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env file")


model = init_chat_model(
    model="google_genai:gemini-2.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are a professional document summarizer. Your task is to read the given document
        and provide a clear, concise, and informative summary. Follow these rules:

        1. Summarize the main points and key ideas of the document.
        2. Keep the summary concise, ideally 3-5 sentences or 5-7 bullet points.
        3. Use clear, simple language suitable for a general audience.
        4. Do not add opinions or information not present in the document.
        5. Highlight important facts, names, dates, or statistics if present.
        6. Maintain the logical flow of the original document.
        7. If the document contains multiple sections, provide a short summary for each section.

        Output format:
        - Either a short paragraph summary OR bullet points, depending on the document type.
    """),
    ("human", "{document}")   # required for Gemini API
])


chain = prompt | model


from PyPDF2 import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def summarize_document(document)->str:
    summary = chain.invoke({"document":document})
    print(summary)

if __name__=="__main__":
    text=read_pdf("Documents/BATA_Policies_Expanded.pdf")
    summarize_document(text)