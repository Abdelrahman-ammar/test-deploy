from langchain_google_genai import ChatGoogleGenerativeAI , GoogleGenerativeAIEmbeddings
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
import os


qwen = ChatOllama(model="qwen2.5")
llama = ChatOllama(model="llama3.2")
qwen_json_mode = ChatOllama(model="qwen2.5" , mode="json")
REDIS_URL= "redis://localhost:6379/0"

google_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
collected_vectorstore = FAISS.load_local("../FinalEmbeddings/VectorStoreGemini" , google_embeddings , allow_dangerous_deserialization=True).as_retriever(kwargs={"k":5})
general_vectorstore_retriever = FAISS.load_local("../FinalEmbeddings/GeneralQuestionsEmbeddings/" , google_embeddings , allow_dangerous_deserialization=True).as_retriever(kwargs={"k":3})

Flag_online = False

online_vectorstore_path = "../TestingNotebooks/ScrapedData"
if os.path.exists(online_vectorstore_path):
    online_vectorstore_retriever = FAISS.load_local(online_vectorstore_path , google_embeddings , allow_dangerous_deserialization=True).as_retriever(kwargs={"k":5})
    
    all_retrievers = EnsembleRetriever(
    retrievers=[
        collected_vectorstore , general_vectorstore_retriever , online_vectorstore_retriever
        ],
    weights= [0.5 , 0.3  , 0.2])

else:
    all_retrievers = EnsembleRetriever(
    retrievers=[
        collected_vectorstore , general_vectorstore_retriever 
        ],
    weights= [0.5 , 0.5])


# print(all_retrievers.invoke("what is the taxa classification of the kemp ridley sea turtle?"))



