import logging

from bs4 import BeautifulSoup as bs

from scraper.src.logger import config_logging


# Configure logging
config_logging()


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

        logging.info(f'Profile info: {developer_info}')

        return developer_info
