import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent


from parse import parse_DATA


def get_html(url:str, save_as_file=False)->requests.Response:
    print(f"Fetching {url}")

    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error: {e}")
        return

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    if save_as_file:
        with open('html.html', 'w') as f:
            f.write(response.text)
            print("Saved as html.html")
    return response

def get_developer_page_info(url:str)->dict:
    response = get_html(url)

    if response is None:
        return dict()

    soup = bs(response.text, 'html.parser')

    # Get developer contact info
    developer_info_list = soup.find('ul', class_='nav flex-column nav_info').find_all('li')

    developer_info_address = developer_info_list[0].text
    developer_info_phone = developer_info_list[1].text
    developer_info_email = developer_info_list[2].text

    # Get developer about info
    developer_about_info = soup.find('div', class_='tab-content').find_all('div', class_='desc')

    developer_about = developer_about_info[0].find('p').text
    developer_speciality_service = developer_about_info[1].find('ul').text
    developer_area = developer_about_info[2].find('ul').text


    return {
        'address': developer_info_address,
        'phone': developer_info_phone,
        'email': developer_info_email,
        'about': developer_about,
        'speciality_service': developer_speciality_service,
        'area': developer_area
    }

def developer_profile()->list[dict]:
    # Get initial data from DATA.py
    initial_data = parse_DATA()
    total_data = len(initial_data)

    for i, developer in enumerate(initial_data):
        print(f"Processing {i+1}/{total_data}")
        url = developer['developer_url']
        developer_contact_info = get_developer_page_info(url)

        # Merge developer contact info with initial data
        developer.update(developer_contact_info)

    return initial_data

def export_developer_profile():
    developer_data = developer_profile()

    df = pd.DataFrame(developer_data)
    df.to_excel('developer_profile.xlsx', index=False)
    print("Saved as developer_profile.xlsx")


def export_project_data():
    # UPDATE THIS REGULARLY
    COOKIES = "visid_incap_2513605=ootZ0OkDQC+WAS2VmiFpanIHGmcAAAAAQUIPAAAAAAA5M9oFurM1hbVMEf1kQrEy; dtCookie=v_4_srv_1_sn_D354AFF1A6F11EF98FC4C489C5AE2337_perc_100000_ol_0_mul_1_app-3A6fd18db7d73f7911_1; TS01bfb558=012d9186a8ecf65f26cb7a476ad6210874178ff60f0750b71ac3cb732b63cb7b45f1f58635a48a120a7a69be4f09473f34c32d528608d839b5130e59f1cad6adb87478759e; _gcl_au=1.1.158046580.1729759092; rxVisitor=1729759091613B0U3J19DBHDFVD3R0IEQKUG16TLJEG5S; _ga=GA1.1.923844190.1729759092; __Host-next-auth.csrf-token=2c8e2404613d1040986464f344b11edf3be9c23d56bcdbfd274bfa3a1b1dbbc6%7C23d12a86a05de3d018ab05730b558dc6a4bb9a2d3a1cfc6b734e42bfca62d64a; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.btnproperti.co.id; _fbp=fb.2.1729759095626.604070392823336712; _tt_enable_cookie=1; _ttp=8TOI-vF7tj2qYg8soYTixZPkpeN; incap_ses_7254_2513605=6TJ6UyxFgRXHKC1mtmKrZM46GmcAAAAAge+vXPFL3FlqM4yCSpNlPg==; _ga_RNT3PCE7FK=deleted; incap_ses_7259_2513605=QHXsZqZBQmJ7kc6oLya9ZAtDGmcAAAAAsRy4Na/GbkQfUpXSksM+bA==; PHPSESSID=34m7ho0j6p55kp9k1d6kbrfvpk; XSRF-TOKEN=eyJpdiI6IkdHSXJLVFNoVlpHYTVBYWp4K0RUdUE9PSIsInZhbHVlIjoiVTJpUjJESDd5UE5aOUVQZyt3UkpRTFpVR2dOdjJxVU1ab3E0bXB6RXlQbjR0RW4ycDZDVjduWDE3ck9FcnZvSzdSMUZiQVN3RGdQMW56TC9sN1dGckNkNEhaR1R5ekIycjlZckFLVHVaVXNHRWIyMlRPTmJ3Q1diMTA2RWNhM2UiLCJtYWMiOiI0MDAzZmU4ODMwMzJkYTI4NjhmNTQ5NzBjN2FkYWUzNzY4N2VhZTU0ZWMxOWQ2NjEwZDZhMjliOTVhZjYwNzBkIiwidGFnIjoiIn0%3D; laravel_session=eyJpdiI6InBzcVFUTUI1and5dXdjWCswMmhSbWc9PSIsInZhbHVlIjoiTW02V0I2SFhxdkEzRFBFeklvWS8waGVQbnJmcU5IaFN4blI1SldHY2RPZUFFZUZ2a1VkMnRXR3pCOERHbEYrRkNmU2RweDFqUHpRQUg5Zmp1d1ZxZkFiTklqN3MrSFRKNVNKZFNaeWZuZWlhY0xaOHkxUUJCTUtJWUc3NTJVc0ciLCJtYWMiOiJlMTU4YTUzMmY1NmM3OTMxM2VjY2VhOGMyYjA2NGFiZGYzZGUxZDM5NGQ2MGFkNmZmODkzZmI3YmI5ZDI3YzgyIiwidGFnIjoiIn0%3D; incap_ses_1116_2513605=X3emYo0I0FkW3XydQtR8D6ZHG2cAAAAAq1+5bKH6pgTgFe8nld3XXg==; dtSa=-; accessKey=3b9b742d-1e34-42f9-825b-f864fda52a41; settings=true; ci_session=r2jpqbnqanf8d5oog35ic0v4n08spun7; TS01e594d7=012d9186a8e13527ad32bdb44a0e9f0b8061ed5168d6b7c1009b181e3722fd8ae4a0de072ebc38af53fec8b939a5ea2527fa50f8d86e12d0d1df2f945c6514db4f3732b5d6f3e9c933ea36b60ddf01594fed35d827886f06ccc1c425feee4e87561c4a3c30d5e3475cbfecc75319100b42ae856a4f2167cdc76403b23fdbf8ac0a04d165be; _ga_RNT3PCE7FK=GS1.1.1729841460.8.1.1729842618.16.0.0; _ga_0T3DNMER8R=GS1.1.1729841460.9.1.1729842619.0.0.0; rxvt=1729844421195|1729841459062; dtPC=1$42619326_947h8vPWHICLBMOHDUKDTMEFUSKVRKUHMTPVFH-0e0"

    session = requests.Session()
    session.headers.update({"cookie": COOKIES})

    data = pd.read_excel('developer_profile.xlsx')
    # data = data.iloc[:10]
    count = len(data)
    print(f"Processing {count} developers.............")

    all_data = []
    for index, row in data.iterrows():
        print(f"Processing {index}/{count}")
        url = row['property_url']
        print(f"Fetching {url}")
        
        response = session.get(url)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            continue
        
        try:
            response_data = response.json()['data']
            all_data.extend(response_data)

        except Exception as e:
            print(f"Error: {e}")
            continue
    
    df = pd.DataFrame(all_data)
    df.to_excel('developer_project_data.xlsx', index=False)
    print("Saved as developer_project_data.xlsx")





if __name__ == "__main__":
    # export_developer_profile()
    export_project_data()