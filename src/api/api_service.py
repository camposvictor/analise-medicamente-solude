import requests
import os
from urllib.parse import quote, urljoin
from dotenv import load_dotenv

load_dotenv()

class ApiService:
    def __init__(self):
        self.base_url = os.environ.get('API_URL')
        self.s = requests.Session()
        self.s.headers.update({'Authorization': f"Bearer {os.environ.get('API_TOKEN')}"})

    def get(self, endpoint, params=None):
        url = urljoin(self.base_url, endpoint)
        print
        try:
            response = self.s.get(url, params=params)

            if response.status_code == 200:
                return response.json()  # You can modify this to return response content in other formats if needed
            else:
                print(f"Request failed with status code {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
api_service = ApiService()