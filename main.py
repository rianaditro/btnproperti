import pandas as pd

from scraper.json_parser import reformat_data
from scraper.blueprint_scraper import WebFetcher, ProfileParser


def main_scraper(cookies:str, json_file:str):
    # Read data from JSON file
    developer_profile = reformat_data(json_file)
    max_counter = len(developer_profile)

    fetcher = WebFetcher(cookies)
    for index, profile in enumerate(developer_profile[0:1]):
        print(f"Processing {index+1} of {max_counter} profiles")
        print(profile)
        developer_url = profile['developer_url']
        project_url = profile['project_url']

        # Parse developer profile
        developer_page = fetcher.get_response(developer_url)
        developer_parser = ProfileParser(developer_page)
        profile_info = developer_parser.profile_info()
        print(profile_info)
        # Merge new data with origin data
        profile.update(profile_info)

        # Parse developer project
        project = fetcher.get_json(project_url)
        print(project)

        yield profile, project
    

def main(cookies:str, json_file:str):
    # Result container
    profiles = []
    projects = []

    # Scrape data
    for profile, project in main_scraper(cookies, json_file):
        profiles.append(profile)
        projects.extend(project)

    # Export as file
    df_profile = pd.DataFrame(profiles)
    df_project = pd.DataFrame(projects)

    df_profile.to_excel('developer_profile.xlsx', index=False)
    df_project.to_excel('developer_project_data.xlsx', index=False)

    print("Done!")


if __name__ == "__main__":
    COOKIES = 'visid_incap_2513605=ootZ0OkDQC+WAS2VmiFpanIHGmcAAAAAQUIPAAAAAAA5M9oFurM1hbVMEf1kQrEy; dtCookie=v_4_srv_1_sn_D354AFF1A6F11EF98FC4C489C5AE2337_perc_100000_ol_0_mul_1_app-3A6fd18db7d73f7911_1; TS01bfb558=012d9186a8ecf65f26cb7a476ad6210874178ff60f0750b71ac3cb732b63cb7b45f1f58635a48a120a7a69be4f09473f34c32d528608d839b5130e59f1cad6adb87478759e; _gcl_au=1.1.158046580.1729759092; rxVisitor=1729759091613B0U3J19DBHDFVD3R0IEQKUG16TLJEG5S; _ga=GA1.1.923844190.1729759092; __Host-next-auth.csrf-token=2c8e2404613d1040986464f344b11edf3be9c23d56bcdbfd274bfa3a1b1dbbc6%7C23d12a86a05de3d018ab05730b558dc6a4bb9a2d3a1cfc6b734e42bfca62d64a; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.btnproperti.co.id; _fbp=fb.2.1729759095626.604070392823336712; _tt_enable_cookie=1; _ttp=8TOI-vF7tj2qYg8soYTixZPkpeN; incap_ses_7254_2513605=6TJ6UyxFgRXHKC1mtmKrZM46GmcAAAAAge+vXPFL3FlqM4yCSpNlPg==; _ga_RNT3PCE7FK=deleted; incap_ses_7259_2513605=QHXsZqZBQmJ7kc6oLya9ZAtDGmcAAAAAsRy4Na/GbkQfUpXSksM+bA==; PHPSESSID=34m7ho0j6p55kp9k1d6kbrfvpk; incap_ses_1116_2513605=X3emYo0I0FkW3XydQtR8D6ZHG2cAAAAAq1+5bKH6pgTgFe8nld3XXg==; incap_ses_7267_2513605=MNTNDzndx2FYCp8cJ5LZZEQWHmcAAAAA9Ioog6PhiZRi2SMdmOWNdA==; incap_ses_7260_2513605=/RZ4CkAUSmKTV3mcsLPAZMzaIGcAAAAACk3+aEXqRAp8okeGos56FQ==; incap_ses_7251_2513605=SnMoaC7J3g1rgqC4PLqgZP7YIWcAAAAA/h4lxm4EDZOu7Pxvql1qpA==; incap_ses_1112_2513605=5MMSKi1qIHMqatlQSp5uD8wFImcAAAAALXVzCn+pYpOLJQx02i2feA==; dtSa=-; accessKey=e9c0bd34-779e-4306-8ca4-e6951d794c4d; settings=true; _ga_0T3DNMER8R=GS1.1.1730282959.21.1.1730282977.0.0.0; ci_session=3aqlk7qj90fg4paggdhlbligj2e69nr1; TS01e594d7=012d9186a8b75344a75d19ad056a658ab09a7d6e37fd02ee675835d2de9717e6475e5a03c70544ca0c908d3ab0959c16631397b66e3d03417d5facc0338e6fb6760c4067c97ba07f580ef8e3f5af6cea4db9880613d503caf25da279c6b81ec8b5ae904ecaff4572823bd192c19b26bec101374ebaed68fef6a4e394cbeacc20625a149a74; _ga_RNT3PCE7FK=GS1.1.1730282958.20.1.1730283160.60.0.0; rxvt=1730284961221|1730282957399; dtPC=1$482974769_905h21vBLWNTUURORABHMFMUMFAURLNVPMMOCBR-0e0'

    main(COOKIES, "DATA.json")
