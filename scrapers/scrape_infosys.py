from bs4 import BeautifulSoup
import requests
import uuid

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://digitalcareers.infosys.com/',
    'DNT': '1'
}

def return_dict(job_title, job_link, location):
    return {
        "id": str(uuid.uuid4()),
        "job_title": job_title,
        "job_link": job_link,
        "company": "Infosys",
        "country": "India",
        "location": location
    }

def get_jobs(title, location):
    list_jobs = []

    for page in range(1, 5):  # Adjust the range as needed
        url = f'https://digitalcareers.infosys.com/infosys/global-careers?page={page}&per_page=25&job_type=experienced'
        response = requests.get(url, headers=DEFAULT_HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')

        jobs = soup.find_all('a', class_='job editable-cursor')
      
        for job in jobs:
            job_link = job.get('href')
            job_title = job.find('div', class_='job-title').text.strip()
            job_location = job.find('div', class_='job-location js-job-city').text.split('-')[0].split()[0].strip(',')
            print(job_title,job_location)
            print(title.lower() in job_title.lower())
            if title.lower() in job_title.lower() and location.lower() in job_location.lower():
                list_jobs.append(return_dict(job_title, job_link, job_location))

    return list_jobs