import json
import re
import requests
from bs4 import BeautifulSoup
import os
from collections import OrderedDict


# Pfade
script_path = os.path.dirname(os.path.realpath(__file__))
json_file_path_in = os.path.join(script_path, "filme_rezensionen.json")
json_file_path_out = os.path.join(script_path, "filme_rezensionen_extendet.json")

def extract_genres(soup):
    genres = []

    
    genre_list = soup.find('div', class_='ipc-chip-list--baseAlt')
    if genre_list:
       
        genre_tags = genre_list.find_all('span', class_='ipc-chip__text')
        for tag in genre_tags:
            genres.append(tag.text.strip())

    return genres

def extract_bewertung_und_anzahl(soup):
    bewertung_container = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
    
    if bewertung_container:
        bewertung_span = bewertung_container.find('span')
        bewertung = bewertung_span.text.strip() if bewertung_span else "xxx"
        
        anzahl_text = bewertung_container.find_next_sibling('div').text if bewertung_container.find_next_sibling('div') else bewertung_container.parent.text
        
        anzahl_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:\s*Mio\.)?)', anzahl_text.replace('.', '').replace(',', ''))
        anzahl = anzahl_match.group(0) if anzahl_match else "ccc"
    else:
        bewertung = "vvv"
        anzahl = "yyy"

    return bewertung, anzahl




# Lese die JSON-Datei ein
with open(json_file_path_in, 'r', encoding='utf-8') as file:
    filme_daten = json.load(file)


for imdb_id, film_details in filme_daten.items():
    url = f'https://www.imdb.com/title/{imdb_id}/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    
    print("Statuscode:", response.status_code)
    # ausgeben der ersten zeichen ...
    print(response.text[:150])
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extrahiere die benötigten Daten
        genres = extract_genres(soup)
        bewertung, anzahl = extract_bewertung_und_anzahl(soup)
        
                
        film_details['kategorie'] = genres
        film_details['gesamtbewertung'] = bewertung
        film_details['globale Bewertungen'] = anzahl



# Speichere das aktualisierte JSON
with open(json_file_path_out, 'w', encoding='utf-8') as file:
    json.dump(filme_daten, file, ensure_ascii=False, indent=4)


print("Metadaten extended.")