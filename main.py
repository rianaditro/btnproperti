import json

import pandas as pd

from scraper.main_scraper import main as scraper
    


def main(HEADERS:str, DATA:str):
    # Scrape data
    profile, project = scraper(HEADERS, DATA)

    # Export as file
    df_profile = pd.DataFrame(profile)
    df_project = pd.DataFrame(project)

    df_profile.to_excel('developer_profile.xlsx', index=False)
    df_project.to_excel('developer_project_data.xlsx', index=False)

    print("Done!")


if __name__ == "__main__":
    main("HEADERS.json", "DATA.json")
