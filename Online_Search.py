from Config import qwen
from scrape_data import web_base_scraper
from langchain.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
import threading

tavily_tool = TavilySearchResults(k=3)

def online_search_agent(query : str):
    search_prompt = PromptTemplate(
    template="""You are a highly skilled Turtles Researcher assistant. You will be provided with multiple excerpts from trusted sources. Your task is to extract and infer the most relevant and precise answer to the given question using only the provided context. 

    ### Important Instructions:
    - The context contains partial readings from webpages and may not always state the answer explicitly. Your job is to synthesize the most relevant information available.
    - If the answer is indirectly mentioned or requires minor inference (such as recognizing numerical ranges or summarizing scattered details), provide a well-formed answer based on the data.
    - Do NOT make up any information. If the exact answer cannot be determined with high confidence, say: "The context does not provide a definitive answer."
    - If multiple sources provide conflicting data, summarize the range of information accurately.

    ### CONTEXT:
    {context}

    ### QUESTION:
    {question}

    ### ANSWER:
    """,
    input_variables=["context", "question"]  
    )

    search_results = tavily_tool.invoke(query)
    print(search_results)

    urls = [dic["url"] for dic in search_results]
    
    answer_collections = [dic["content"] for dic in search_results]

    context = f"""Source 1 : \n {answer_collections[0]} \n Source 2 : \n {answer_collections[1]} \n Source 3 : \n {answer_collections[2]} \n Source 4 : \n {answer_collections[3]} \n Source 5 : \n {answer_collections[4]}"""


    print(f"Context is : {context}")
    online_search_agent = search_prompt | qwen

    print(online_search_agent.invoke({"context" : context , "question" : query}).content)
    # scrape_thread = threading.Thread(target =web_base_scraper  , args =(urls,))

online_search_agent("what is the hearing range of the flatback sea turtle?")