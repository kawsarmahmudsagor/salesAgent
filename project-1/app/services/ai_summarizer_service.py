from langchain.chat_models import init_chat_model
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate

from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
from helpers.convert_to_text import convert_to_txt

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
        You are a professional document summarizer and meta tag generator. Your task is to read the given document
    and produce two outputs:

    1. **Summary:** A clear, concise, and informative summary of the document.
    2. **Meta Tags:** 3-7 concise hashtags suitable for social media (e.g., Twitter), capturing the main topics.

    Follow these rules:

    **Summary Rules:**
    - Summarize the main points and key ideas.
    - Keep it concise: 3-5 sentences or 5-7 bullet points.
    - Use simple, clear language suitable for a general audience.
    - Do not add opinions or information not present in the document.
    - Highlight important facts, names, dates, or statistics if present.
    - Maintain the logical flow of the original document.
    - If the document has multiple sections, provide a short summary for each.

    **Meta Tags Rules:**
    - Generate 3-7 hashtags that represent the key topics.
    - Each tag must start with `#`.
    - Tags should be short, clear, and relevant.
    - Avoid generic or vague tags.
    - Return tags as a comma-separated list, without extra text.

    **Output Format:**
    - First, the summary (paragraph or bullet points).
    - Then, a line labeled `Tags:` followed by the comma-separated hashtags.
    """),
    ("human", "{document}")   # required for Gemini API
])


chain = prompt | model

def tags_generate_summarize_document(document_path) -> tuple[str, str]:
    text = convert_to_txt(document_path)
    
    result = chain.invoke({"document": text})
    
    # Make sure we work with the actual string content
    content = result.content  # AIMessage -> string

    # Parse summary and tags
    if "Tags:" in content:
        summary_text, tags_line = content.split("Tags:", 1)
        summary_text = summary_text.strip()
        tags_line = tags_line.strip()
    else:
        summary_text = content.strip()
        tags_line = ""
    
    return summary_text, tags_line

