from langchain_core.prompts import ChatPromptTemplate
from Config import qwen , REDIS_URL
from tools import search_photos_tool , retriever_tool
from langchain.agents import create_tool_calling_agent , AgentExecutor
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from utils import get_message_history



prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a helpful assistant , if you don't find an answer in a tool then you should search online using the search tool , DO NOT ANSWER FROM YOUR OWN KNOWLEDGE"
   "always respond like you are in a conservation , REMEBER DO NOT USE YOUR OWN KNOWLWDGE"),
  ("placeholder", "{chat_history}"),
  ("human", "{input}"),
  ("placeholder", "{agent_scratchpad}"),
])


tools = [search_photos_tool , retriever_tool]

agent = create_tool_calling_agent(qwen , tools , prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True , return_intermediate_steps=True)

 
agent_with_message_history = RunnableWithMessageHistory(
    agent_executor,
    get_message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

answer = agent_with_message_history.invoke({"input": "can you show me one photo for it please?"} , config={"configurable" : {"session_id":"3awady"}})

# print(anwer["content"])
print(answer["output"])


# AI agents ==> langchain , langgraph , Llamaindex , phidata
