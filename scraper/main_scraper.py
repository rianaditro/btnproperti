from scraper.src.json_parser import reformat_data
from scraper.src.web_fetcher import WebFetcher
from scraper.src.profile_page_parser import ProfileParser


def parse_profile(fetcher:WebFetcher, developer_url:str)->dict:
    # Get HTML text
    profile_page = fetcher.get_profile(developer_url)
    # Parse data
    profile_info = ProfileParser(profile_page).profile_info()

    return profile_info
    
def main(HEADERS:str, DATA:str):
    # Read data from JSON file
    profile = reformat_data(DATA)

    # To track scraping progress
    counter = len(profile)

    # Container all result
    projects = []

    fetcher = WebFetcher(HEADERS)
    for index, developer in enumerate(profile):
        print(f"Processing {index+1} of {counter} profiles")
        developer_url = developer['developer_url']
        project_url = developer['project_url']

        # Parse developer profile
        profile_info = parse_profile(fetcher, developer_url)
        # Merge new data with origin data
        developer.update(profile_info)

        # Parse developer project
        project = fetcher.get_project(project_url)
        projects.extend(project)
    
    return profile, projects

    