import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Pfad
script_path = os.path.dirname(os.path.realpath(__file__))

def get_review_page_urls(source):
    """
    Extrahiert FilmURLs von einer gegebenen IMDB-Seite oder lokalen Kopie einer IMDB Datei im HTML Format
    
    Args:
    source (str): Die URL der IMDB-Seite oder der Pfad zur lokalen HTML-Datei.

    Returns:
    set: Ein Set von extrahierten Film-URLs.
    """
    
    # Überprüfen, ob die Quelle eine URL oder ein lokaler Pfad ist
    parsed_url = urlparse(source)
    if parsed_url.scheme in ('http', 'https'):
        # Verarbeitung der URL
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(source, headers=headers)
        if response.status_code != 200:
            raise Exception(f"HTTP-Anfrage fehlgeschlagen mit Statuscode: {response.status_code}")
        content = response.content
    else:
        # verarbeitung der lokalen HTMLDatei
        with open(source, 'r', encoding='utf-8') as file:
            content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    ul = soup.find('ul', class_='ipc-metadata-list')
    if not ul:
        raise Exception("Seite enthält nicht das erwartete Tag")

    review_urls = set()
    for div in ul.find_all('div', class_='ipc-title'):
        a_tag = div.find('a', href=True)
        if a_tag:
            match = re.search(r'/title/(tt\d+)/', a_tag['href'])
            if match:
                film_id = match.group(1)
                #erzeugen Url mit allen gewünschten Filtern über Parameter
                review_url = f"https://www.imdb.com/title/{film_id}/reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter=0"
                review_urls.add(review_url)
        else:
            print(f"Kein a-Tag gefunden in div: {div}")
    return review_urls

def save_urls_to_file(review_urls, file_name):
    """
    Speichert die übergebenen URLs in eine Datei.

    Args:
    review_urls (set): Die Menge von URLs, die gespeichert werden sollen.
    file_name (str): Der Name der Datei, in die die URLs gespeichert werden sollen.
    """
    with open(os.path.join(script_path, file_name), 'w', encoding='utf-8') as file:
        for link in review_urls:
            file.write(link + '\n')

# AusgangsURL oder lokale Datei
#imdb_url = os.path.join(script_path, 'imdbMostRated.html')
# Alternativ: 
imdb_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
# Oder: imdb_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

# Links extrahieren und in eine Datei speichern
movie_links = get_review_page_urls(imdb_url)
save_urls_to_file(movie_links, '0_imdb_movie_urls.txt')