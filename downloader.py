import os
import requests
import time
import re
from bs4 import BeautifulSoup as bs
import random
import string
from tqdm import tqdm

def generate_random_filename(extension=".bin", length=8):
    characters = string.ascii_letters + string.digits
    random_name = ''.join(random.choice(characters) for _ in range(length))
    return f"{random_name}{extension}"

def fix_url_scheme(url):
    if not re.match(r'^https?://', url):
        url = 'http://' + url.lstrip('/')
    return url

def clean_file_name(file_name):
    cleaned_name = re.sub(r'_--_fitgirl-repacks\.site_--_', '', file_name)
    cleaned_name = cleaned_name.strip()
    return cleaned_name

def getlink(link, file_name):
    folder_name = 'Games'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    if not file_name:
        file_name = generate_random_filename()

    file_extension = os.path.splitext(file_name)[-1]
    if not file_extension:
        file_extension = '.bin'

    file_path = os.path.join(folder_name, file_name)
    temp_file_path = file_path + '.temp'

    if os.path.exists(file_path):
        return

    print(f"Preparing to download file: {file_name}")

    try:
        response = requests.get(link, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return

    print(f"Downloading file {file_path}")

    total_length = response.headers.get('content-length')
    total_length = int(total_length) if total_length is not None else None

    with open(temp_file_path, 'wb') as f, tqdm(
        desc=file_name,
        total=total_length,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        ncols=100
    ) as pbar:
        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))

    time.sleep(1)
    os.rename(temp_file_path, file_path)
    print(f"File successfully saved to: {file_path}")

def get_file_name(game_url: str):
    response = requests.get(game_url)
    soup = bs(response.text, 'html.parser')
    span = soup.find('span', class_='text-xl')
    if span:
        raw_file_name = span.get_text(strip=True)
        return clean_file_name(raw_file_name)
    return None

def getjavascripturls(game_url: str):
    response = requests.get(game_url)
    soup = bs(response.text, 'html.parser')
    scripts = soup.find_all('script')
    urls = []
    for script in scripts:
        if script.string:
            matches = re.findall(r'window\.open\(["\'](https?://[^\s"\']+)["\']', script.string)
            urls.extend(matches)
    return urls

def downloadLinks(game_name: str):
    url = f"https://fitgirl-repacks.site/{game_name}"
    response = requests.get(url)
    html_content = response.text
    soup = bs(html_content, 'html.parser')
    links = soup.find_all('a')
    downloaded_urls = set()

    if len(links) == 1:
        game_link = links[0].get('href')
        if game_link:
            game_link = fix_url_scheme(game_link)
            javascript_urls = getjavascripturls(game_link)
            for url in javascript_urls:
                url = fix_url_scheme(url)
                if url not in downloaded_urls:
                    downloaded_urls.add(url)
                    file_name = get_file_name(game_link)
                    if not file_name:
                        file_name = generate_random_filename()
                    getlink(url, file_name)
        return

    for link in links:
        game_link = link.get('href')
        if game_link and "fuckingfast.co/" in game_link:
            game_link = fix_url_scheme(game_link)
            javascript_urls = getjavascripturls(game_link)
            for url in javascript_urls:
                url = fix_url_scheme(url)
                if url not in downloaded_urls:
                    downloaded_urls.add(url)
                    file_name = get_file_name(game_link)
                    if not file_name:
                        file_name = generate_random_filename()
                    getlink(url, file_name)