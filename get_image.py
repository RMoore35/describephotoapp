import os
import time
import requests
from urllib.parse import quote
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("accessKey")

def get_random_image_url(keyword="nature"):
    url = "https://api.unsplash.com/photos/random"
    headers = {"Accept-Version": "v1"}
    params = {
        "client_id": ACCESS_KEY,
        "query": keyword,
        "orientation": "landscape"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["urls"]["regular"]