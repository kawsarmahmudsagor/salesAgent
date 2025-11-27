from langchain_community.vectorstores import Chroma

vectordb = Chroma(persist_directory="embeddings")
retriever = vectordb.as_retriever()
print(dir(retriever))  # see available methods
