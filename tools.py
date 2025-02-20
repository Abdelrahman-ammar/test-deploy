from utils import search_photos
from langchain.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from Config import all_retrievers

search_photos_tool = Tool(
    name="Photos_tool",
    func=search_photos,
    description="Tool used for photos , any photos queries you must use this tool"
)


retriever_tool = create_retriever_tool(retriever=all_retrievers , name="Turtles_Researcher" ,
                                        description="Searches for information about the turtles , for any questions regarding the turtles you should use this tool! ")



