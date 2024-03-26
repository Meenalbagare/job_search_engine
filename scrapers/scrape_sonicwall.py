from bs4 import BeautifulSoup
import requests
import uuid

DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://google.com',
        'DNT': '1'
    }

def return_lst_dict(title: str, link: str, location: str) -> dict:
    '''
    ... this function will return a dict to append to a list and avoid DRY
    '''
    dct = {
                "id": str(uuid.uuid4()),
                "job_title": title,
                "job_link": link,
                "company": "Sonicwall",
                "country": "India",
                "location": location
            }
    
    return dct

def scrape_sonicwall(title: str, location: str):
    url = f'https://boards.greenhouse.io/sonicwall?q=%7Btitle%7D'
    response = requests.get(url, headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div',class_='opening')
    lst_with_data = []
    for sd in soup_data:
        link ='https://boards.greenhouse.io' + sd.find('a')['href']
        job_title = sd.find('a').text
        job_location = sd.find('span', class_='location').text.strip()
        if location.lower() in job_location.lower()  and title.lower() in job_title.lower() :
            lst_with_data.append(return_lst_dict(title=job_title, link=link, location=job_location))
            
    
    return lst_with_data