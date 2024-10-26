from DATA import DATA


def parse_DATA()->list[dict]:
    # Read DATA from DATA.py
    data = DATA["data"]

    base_url = "https://www.btnproperti.co.id/"
    get_property_url = "api-partners/open-api/v1/manstok/getProperByDevId"
    
    # Parse developer data
    developer_data = []

    for developer in data:
        developer_url = f"{base_url}developer/detail/{developer['n'].lower().replace(' ', '-')}-{developer['id'].lower()}"
        property_url = f"{base_url}{get_property_url}?dev_id={developer['id']}&Page=1&Limit=50"

        # Add URL for scraping
        developer['developer_url'] = developer_url
        developer['property_url'] = property_url

        developer_data.append(developer)

    return developer_data




if __name__ == "__main__":
    print(parse_DATA()[-1])
    
