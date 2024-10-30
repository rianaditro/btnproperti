import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup as bs



class WebFetcher:
    def __init__(self, cookies:str=None):
        self.session = requests.session()
        self.session.headers.update(
            {"cookie": cookies}
        )
        self.failed_urls = []

        # Retry connection when failed
        retry = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('https://', adapter)
    
    def error_handling(self, url:str, e:Exception):
        print(f"Failed to fetch {url}: {e}")

        message = {
            'url': url,
            'message': str(e)
            }
        
        self.failed_urls.append(message)
        return None

    def get_response(self, url:str)->requests.Response:
        print(f"Fetching {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        
        except Exception as e:
            return self.error_handling(url, e)

    def get_json(self, url:str)->dict:
        print(f"Fetching {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            data = data['data']
            return data
        
        except Exception as e:
            return self.error_handling(url, e)


class ProfileParser:
    """
    Combine data from provided JSON file with page parsed from profile URL
    """
    def __init__(self, response_content:str):
        self.soup = bs(response_content, 'html.parser')

    def profile_info(self)->dict:
        developer_info_list = self.soup.find('ul', class_='nav flex-column nav_info').find_all('li')

        # Get developer contact info
        developer_info_address = developer_info_list[0].text
        developer_info_phone = developer_info_list[1].text
        developer_info_email = developer_info_list[2].text

        # Get developer about info
        developer_about_info = self.soup.find('div', class_='tab-content').find_all('div', class_='desc')

        developer_about = developer_about_info[0].find('p').text
        developer_speciality_service = developer_about_info[1].find('ul').text
        developer_area = developer_about_info[2].find('ul').text

        developer_info = {
            'address': developer_info_address,
            'phone': developer_info_phone,
            'email': developer_info_email,
            'about': developer_about,
            'speciality_service': developer_speciality_service,
            'area': developer_area
        }

        return developer_info
