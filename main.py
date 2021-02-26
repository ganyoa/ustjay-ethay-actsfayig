"""
scrape and mashup
scrape random quote from http://unkno.com
mashup in pig latinizer https://hidden-journey-62459.herokuapp.com/

"""

import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    """
    scrape random fact from unkno website
    """
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_pig(fact):
    """
    fuction to utilize get_fact() as an arguement (the random fact) and
    return the url result from the pig latinizer app
    """
    payload = {'input_text': fact}
    response = requests.post(
                             'https://hidden-journey-62459.herokuapp.com/piglatinize/',
                              allow_redirects=False,
                              data=payload)

    return response.headers['Location']

@app.route('/')
def home():
    """
    the random fact retrieved from get_fact() becomes the arguement
    in get_pig(fact) and subsequently the input_text into the pig latinizer
    """
    return Response(response=get_pig(get_fact()))



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

