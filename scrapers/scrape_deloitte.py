from bs4 import BeautifulSoup
import requests
import uuid
from requests_html import HTMLSession
DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }
def make_bs4_object(requests_html_object) -> BeautifulSoup:
    '''
    Convert requests-html to bs4 object.
    '''
    return BeautifulSoup(requests_html_object, 'lxml')

def config_requests_html() -> HTMLSession:
    '''
    Config requests_html with headers and make new requests
    and parse js data.
    '''

    session = HTMLSession()
    session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    session.headers['Accept-Language'] = 'en-US,en;q=0.5'
    session.headers['Refer'] = 'https://google.com/'
    session.headers['DNT'] = '1'

    return session

def scrape_deloitte(title, location):
    session = config_requests_html()
    page_jobs = 1
    max_pages = 50  # Limit the number of pages to scrape
    lst_with_data = []

    while page_jobs <= max_pages:
        try:
            response = session.get(url=f'https://apply.deloitte.com/careers/SearchJobs/{title}?listFilterMode=1&jobSort=relevancy&jobRecordsPerPage=10&sort=relevancy', timeout=10)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print(f"Request timed out for page {page_jobs}")
            break
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            break

        job_elements = response.html.find('article.article--result')
        if not job_elements:
            break

        for job in job_elements:
            soup_bs4 = make_bs4_object(job.html)
            job_title = soup_bs4.find('a').text.strip()
            job_location = soup_bs4.find('span').text.strip()  # Assuming location is in a specific span
            
            if title.lower() in job_title.lower() or location.lower() in job_location.lower():
                link = soup_bs4.find('a')['href']
                lst_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": job_title,
                    "job_link": link,
                    "company": "Deloitte",
                    "country": location,  # Change as per actual data
                    "location": job_location,  # Use actual location data
                   
                })
            
        page_jobs += 10
        
    return lst_with_data