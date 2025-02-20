import random
import json
import requests
from Config import REDIS_URL
from langchain.tools import tool
from langchain_community.chat_message_histories import RedisChatMessageHistory



def prepare_content(output):
    if isinstance(output, dict):
        # Serialize dictionary into JSON format
        return json.dumps(output, indent=2)
    return str(output)


def get_taxa_id(query):
    base_url = "https://api.inaturalist.org/v1/taxa"

    params = {"q": query}
    
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json() 
    
    results = data["results"]
    if results :
        return results[0]["id"]

    return {"error": "Please provide a valid query"}


@tool
def search_photos(query , number_of_photos = 3 , page = 2):
    """
    Any query related to photos you must use this tool

    Args:

    query : the species name.
    number_of_photos :  number of photos to search and return.
    """
    
    taxon_id = get_taxa_id(query)

    base_url = "https://api.inaturalist.org/v1/observations"
    
    params = {
            "taxon_id": taxon_id,
            "per_page": number_of_photos,
            "page": page,
        }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("Please Provide a valid query or species")
        # print(f"Failed to fetch data for page {page}: {response.status_code}")

    data = response.json()
    
    results = data.get("results", [])
    
    if not results:
        print(f"No more results found on page {page}.")

    photos2 = []
    for obs in results:
        photos = obs.get("photos", [])
        for photo in photos:
            image_url = photo.get("url")
            if image_url:
                photos2.append(image_url.replace("square" , "original"))

    if photos2:
        final_photos = random.sample(photos2 , int(number_of_photos))
        return prepare_content({"photos":final_photos})
    

    return {"error": "Please provide a valid query"}


def get_message_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)