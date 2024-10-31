import json
import logging

from scraper.src.logger import config_logging


# Configure logging
config_logging()



def reformat_data(json_file:str)->list[dict]:
    """
    Parse data from provided JSON file
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
        data = data["data"]

    BASE_URL = "https://www.btnproperti.co.id/"
    API_PROJECT_DEVELOPER = f"{BASE_URL}api-partners/open-api/v1/manstok/getProperByDevId"

    # Parse developer profile
    developer_profile = []

    for developer in data:
        profile_url = f"{BASE_URL}developer/detail/{developer['id'].lower()}"
        project_url = f"{API_PROJECT_DEVELOPER}?dev_id={developer['id']}&Page=1&Limit=50"

        # Add URL for scraping
        developer['profile_url'] = profile_url
        developer['project_url'] = project_url

        # Collected data
        logging.info(f"Data Updated: {developer}")

        developer_profile.append(developer)
        
    print("File successfully parsed")
    return developer_profile 
