import logging
import json

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("scraper.log"),
        # logging.StreamHandler() # Console output
    ]
)


class WebFetcher:
    def __init__(self, HEADERS:str):
        """ Needed cookies to access the website """
        with open(HEADERS, 'r') as f:
            HEADERS = json.load(f)
        self.session = requests.session()
        self.session.headers.update(HEADERS)

        # Retry connection when failed
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[400, 429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
    
    def page_handler(self, url:str)->requests.Response:
        """ Handle request and response"""
        logging.info(f"Fetching {url}")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response
        
        except Exception as e:
            if response.status_code == 404: # This might because the developer has no listing project
                logging.info(f"404: No Data for {url}")
            else:
                logging.warning(e)
            return None

    def get_profile(self, url:str)->str:
        """ Get HTML text from profile URL """
        return self.page_handler(url).text
    
    def get_project(self, url:str)->dict:
        """ Get JSON data from project API URL """
        try:
            data = self.page_handler(url).json()
            data = data['data'] # The actual data is in the 'data' key
            return data

        except AttributeError:
            logging.warning(f"Failed to fetch {url}")
            return []
