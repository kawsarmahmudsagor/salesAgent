from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="google_genai:gemini-2.5-flash-lite",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a virtual sales assistant in an e-commerce store. "
               "Converse with users as if you are a real-life sales assistant: friendly, professional, and approachable. "
               "Be formal and don't joke around too much."
               "Proactively suggest products or promotions based on the user's previous interactions and purchase history. "
               "Anticipate the user's needs, ask clarifying questions politely, and make personalized recommendations. "
               "Keep conversations natural and engaging, as if the user is talking to a knowledgeable and personable sales expert."),
    ("human", "{question}")
])

chain = prompt | model

def handle_conversation(history: str, question: str):
    response = chain.invoke({"history": history, "question": question})
    ai_text = response.content
    new_history = history + f"\nUser: {question}\nAI: {ai_text}"
    return ai_text, new_history
