from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)
CORS(app)

def scrape_quotes():
    url = "https://www.azquotes.com/quote_of_the_day.html"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes_elements = soup.find_all('a', class_='title')
        quotes = [quote.get_text().strip() for quote in quotes_elements]
        return quotes
    else:
        return ["Failed to fetch quotes"]

def get_random_quote(quotes):
    if quotes:
        return random.choice(quotes)
    else:
        return "No quotes available"

@app.route('/api/motivational-quotes', methods=['GET'])
def get_motivational_quote():
    quotes = scrape_quotes()
    random_quote = get_random_quote(quotes)
    
    return jsonify({'quote': random_quote})

if __name__ == '__main__':
    app.run(debug=True)
