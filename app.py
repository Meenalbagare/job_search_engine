from flask import Flask, render_template, request
from scrapers.scrape_deloitte import *
from scrapers.scrape_stripe import *
from scrapers.scrape_sonicwall import *

app = Flask(__name__)


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
