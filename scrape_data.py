from langchain_core.prompts import PromptTemplate
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from Config import llama , qwen
from langchain_core.output_parsers import JsonOutputParser , StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveJsonSplitter , CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain.schema import Document
from Config import online_vectorstore_path ,  google_embeddings 
from langchain_community.document_loaders import WebBaseLoader
import asyncio
import os 






# vectorstore = None

# if os.path.exists(online_vectorstore_path):
#     vectorstore = FAISS.load_local(online_vectorstore_path, google_embeddings , allow_dangerous_deserialization=True)

# splitter = RecursiveJsonSplitter(max_chunk_size=500 , min_chunk_size=200)


# from pydantic import BaseModel , Field

# class CleanedData(BaseModel):
#     cleaned : dict[str , str] = Field(... , title="Cleaned Data" , description="a cleaned data from the crawled data")


# def clean_crawled(data):

#     clean_prompt = """
#         You are an intelligent data extraction assistant specialized in turtles. You will be provided with a large amount of markdown data. Your task is to extract only the most useful and relevant details about turtles while preserving the original wording exactly as found in the source.

#         Do not rephrase, summarize, or modify the extracted text in any way—only filter and return the information. Focus on key facts, behaviors, habitats, conservation status, unique characteristics, and any other useful details related to turtles. Ignore unrelated content, duplicates, and unnecessary filler.

#         Return the extracted information as a structured json data that can be suitable for storing in vectorstores , Return the extracted information as a well-structured JSON object where the keys represent meaningful topics or categories, and the values contain the relevant information found in the data.
#         Ensure the JSON remains organized , readable and useful for a general audience interested in turtles, also Remove any links you find.
    
        
#         CRAWLED DATA : {crawled_data}
#     """
#     clean_template = PromptTemplate(template=clean_prompt , input_variables= ["crawled_data"])

#     clean_chain = ( 
#         clean_template
#         | qwen
#         | JsonOutputParser() )
#         # | StrOutputParser())
    
#     cleaned_data = clean_chain.invoke({"crawled_data" : data})
#     print(f"cleaned data -------- {cleaned_data}")
#     return cleaned_data

# non_html_extensions = ['.pdf', '.docx', '.jpg', '.png', '.zip', '.exe']

# def scrape_urls(urls : list):
#     loop =  asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)

#     print(urls)
#     async def async_scrape(urls : list):
#         global vectorstore
#         broswer_conf = BrowserConfig(headless=True)
#         run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

#         filtered_urls = [
#             url for url in urls if not any(url.lower().endswith(ext) for ext in non_html_extensions)
#         ]
#         async with AsyncWebCrawler(config=broswer_conf) as crawler :
#             for i ,url in enumerate(filtered_urls,1):
#                 result = await crawler.arun(url=url , config= run_conf)
#                 print(f"---Url {i}------")
#                 cleaned_data = clean_crawled(result.markdown)
#                 # print(cleaned_data)
#                 print("----------------")
#                 if i == 2:
#                     break
#                 # chunks = splitter.split_json(cleaned_data)
#                 # documents = [Document(page_content=str(chunk)) for chunk in chunks]

#                 # if vectorstore is None:
#                 #     vectorstore = FAISS.from_documents(documents , embeddings)
#                 #     vectorstore.save_local(vectorstore_path)
#                 #     # vectorstore.save_local("ScrapedData /")

#                 # else :

#                 #     vectorstore = FAISS.load_local(vectorstore_path , embeddings , allow_dangerous_deserialization=True)
#                 #     # vectorstore = FAISS.load_local("ScrapedData/" , embeddings , allow_dangerous_deserialization=True)
#                 #     vectorstore.add_documents(documents)
#                 # print(f"---Adding URL {i} in the vector store")

#     loop.run_until_complete(async_scrape(urls))


def web_base_scraper(urls : list):
    for url in urls:
        loader = WebBaseLoader(url)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        print(chunks) 

# web_base_scraper(["https://aqua.org/stories/2024-03-13-mistaken-identities-loggerhead-vs-green-sea-turtles"])