import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from scraper.src.json_parser import reformat_data
from scraper.src.web_fetcher import WebFetcher
from scraper.src.profile_page_parser import ProfileParser
from scraper.src.logger import config_logging


# Configure logging
config_logging()


def parse_profile(fetcher:WebFetcher, profile_url:str)->dict:
    # Get HTML text
    profile_page = fetcher.get_profile(profile_url)
    # Parse data
    profile_info = ProfileParser(profile_page).profile_info()

    return profile_info

def execute_row(fetcher:WebFetcher, row:tuple):
    profile_url = row[0]
    project_url = row[1]
    
    profile_info = parse_profile(fetcher, profile_url)
    project_info = fetcher.get_project(project_url)

    return profile_info, project_info
    
def main(HEADERS:str, DATA:str):
    # Read data from JSON file
    profiles = reformat_data(DATA)
    urls = [(profile['profile_url'], profile['project_url']) for profile in profiles]
    urls= urls[:50]

    # Container all result
    result_projects = []
    result_profiles = []

    fetcher = WebFetcher(HEADERS)

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(execute_row, fetcher, url) for url in urls}

        max = len(urls)
        counter = 1

        for future in as_completed(futures):

            profile, project = future.result()

            profiles[counter-1].update(profile)
            result_projects.extend(project)

            logging.info(f"Profile: {profiles[counter-1]}")

            print(f"Progress: {counter}/{max}... ({counter/max*100:.2f}%)")
            counter += 1

    return profiles, result_projects

    