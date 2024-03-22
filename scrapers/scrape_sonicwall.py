
from bs4 import BeautifulSoup
import requests
import uuid

DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
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
                "city": location
            }
    
    return dct

def scrape_sonicwall():
    response = requests.get(url='https://boards.greenhouse.io/sonicwall?q={title}', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    soup_data = soup.find_all('div',class_='opening')
    
    lst_with_data = []
    for sd in soup_data:
        link ='https://boards.greenhouse.io' + sd.find('a')['href']
        title = sd.find('a').text
        location = sd.find_all('span', class_='location')[-1].text.strip()

        if 'India' in location:
            lst_with_data.append(return_lst_dict(title=title, link=link, location=location))
    
    return lst_with_data