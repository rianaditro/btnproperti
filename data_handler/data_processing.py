import pandas as pd

from scraper.blueprint_scraper import get_developer_page_info


def fill_incomplete_data(df:pd.DataFrame)->pd.DataFrame:

    # Take the developer URL from the missing data
    missing_data_df = df[df['about'].isnull()]

    for index, row in missing_data_df.iterrows():
        url = row['developer_url']
        developer_info = get_developer_page_info(url)

        if developer_info:
            # Merge developer contact info with initial data
            row['address'] = developer_info['address']
            row['phone'] = developer_info['phone']
            row['email'] = developer_info['email']
            row['about'] = developer_info['about']
            row['speciality_service'] = developer_info['speciality_service']
            row['area'] = developer_info['area']

            # Assigning filled row to origin dataframe
            df.loc[index] = row

    # Save to file
    df.to_excel('developer_profile_filled.xlsx', index=False)
    return df




       

if __name__ == "__main__":
    pass