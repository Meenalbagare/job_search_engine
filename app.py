# # app.py
# from flask import Flask, render_template, request
# import requests
# from bs4 import BeautifulSoup


# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/search', methods=['POST'])
# def search():
#     title = request.form['title']
#     location = request.form['location']
#     indeed_results = scrape_deloitte(title, location)
#     # google_results = scrape_google(title, location)
#     # microsoft_results = scrape_microsoft(title, location)
    
#     # all_results = indeed_results + google_results + microsoft_results
#     all_results = indeed_results
#     return render_template('results.html', results=all_results)

# def scrape_deloitte(title, location):
#     # scrape indeed for jobs with given title and location
    


# # Implement scrape_google and scrape_microsoft functions similarly

#  if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests
import uuid
import time
from requests_html import HTMLSession
app = Flask(__name__)
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
                    "country": "India",  # Change as per actual data
                    "location": job_location  # Use actual location data
                    
                })
            
        page_jobs += 10
        
    return lst_with_data

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
                    "country": "Bengaluru",  # You may adjust this as needed
                    "city": job_location  # You may adjust this as needed
                })
    return list_of_jobs


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    title = request.form['title']
    location = request.form['location']
    deloitte_results = scrape_deloitte(title, location)
    stripe = scrape_stripe(title, location)
    sonicwall=scrape_sonicwall()
    all_results = deloitte_results+stripe+sonicwall
    return render_template('results.html', results=all_results)

if __name__ == '__main__':
    app.run(debug=True)
