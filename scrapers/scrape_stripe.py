
from bs4 import BeautifulSoup
import requests


DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Refer': 'https://google.com',
        'DNT': '1'
    }
def scrape_stripe(title, location):
    
    list_of_jobs = []
    response = requests.get('https://stripe.com/jobs/search?office_locations=Europe--Bengaluru', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')

    jobs = soup.find_all('tr', class_='TableRow')

    for job in jobs:
        try:
            link = 'https://stripe.com' + job.find('a').get('href')
        except:
            link = None

        if link is not None and 'jobs/' in link:
            job_title = job.find('a').text.strip()
            job_location = job.find('span', class_='JobsListings__locationDisplayName').text.split(',')[0]
            # Check if the job title and location match the provided title and location
            
            if title.lower() in job_title.lower() and location.lower() in job_location.lower():
                list_of_jobs.append({
                    "job_title": job_title,
                    "job_link": link,
                    "company": "stripe", 
                    "location": job_location 
                })
    return list_of_jobs