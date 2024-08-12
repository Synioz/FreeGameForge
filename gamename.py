import requests
from bs4 import BeautifulSoup

def game_Name(game_name: str):
    url = "https://fitgirl-repacks.site/{}".format(game_name)
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    h1_tag = soup.find('h1', class_='entry-title').text
    return h1_tag