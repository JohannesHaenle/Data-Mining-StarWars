import os
import re
import json
from bs4 import BeautifulSoup

# Pfade für Ein/Ausgabe
script_path = os.path.dirname(os.path.realpath(__file__))
quell_verzeichnis = os.path.join(script_path, "exportFullHtml")
json_dateipfad = os.path.join(quell_verzeichnis, "filme_rezensionen_new.json")

# Datenstruktur initialisieren
filme_daten = {}

def extract_titel_jahr(file_path):
    """
    Extrahiert den Titel, das Jahr und die Summe der Rezensionen aus einer HTML-Datei.

    :param file_path: Der Pfad zur HTML-Datei, die analysiert werden soll.
    :return: Ein Tupel bestehend aus dem extrahierten Titel (str), dem Jahr (str) und der Summe der Rezensionen (str).
             Falls der Titel nicht gefunden werden kann, wird "Fehler beim Auslesen" gesetzt.
             Falls das Jahr nicht ausgelesen werden kann, wird der "xxxx" als Standardwert gesetzt
             Falls die Summe der Rezensionen nicht gefunden wird "yy" als Wert gesetzt.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        #titel
        titel_tag = soup.find('h3', itemprop="name")
        if titel_tag and titel_tag.a:
            titel = titel_tag.a.text.strip()
        else:
            titel = "Fehler beim Auslesen"
        
        # Jahr
        jahr = "xxxx"  # Standardwert, falls keine Jahreszahl gefunden wird
        jahr_tag = titel_tag.find('span', class_="nobr") if titel_tag else None
        if jahr_tag:
            jahr_raw = jahr_tag.text.strip()
            
            match = re.search(r'\b(\d{4})\b', jahr_raw)
            if match:
                jahr = match.group(1)
        
        #summe Rezessionen
        sumrez_tag = soup.find('div', class_='header').find('div')
        if sumrez_tag:
            sumrez_text = sumrez_tag.text.strip()
            sumrez = ''.join(filter(str.isdigit, sumrez_text))
        else:
            sumrez = "yy"
                
        return titel, jahr, sumrez
    
def extract_rezensionen(file_path):
    """
    Extrahiert Rezensionen aus einer lokalen HTML-Datei und gibt Werte als Liste von Dictionaries zurück.

    :param file_path: Der Pfad zur HTML-Datei, welche die Rezensionen enthält.
    :return: Eine Liste von Dictionaries, wobei jedes Dictionary eine Rezension repräsentiert.
             Jedes Dictionary enthält die folgenden Schlüssel:
             - "data-review-id": Die ID der Rezension (str)
             - "username": Der Benutzername des Rezensenten (str)
             - "rating": Die Bewertung der Rezension (str)
             - "date": Das Datum der Rezension (str)
             - "title": Der Titel der Rezension (str)
             - "text": Der Text der Rezension (str)
             Sollte ein Wert nicht gefunden werden wird jeweils "N/A" gesetzt.
    """
    rezensionen = []

    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        # Finde den Hauptcontainer für Rezensionen
        lister_list = soup.find('div', class_='lister-list')
        if lister_list:
            # Finde alle Rezensions-Items
            lister_items = lister_list.find_all('div', class_='lister-item')

            for item in lister_items:
                data_review_id = item['data-review-id'] if 'data-review-id' in item.attrs else "N/A"
                
                username = item.find('span', class_='display-name-link').a.text.strip() if item.find('span', class_='display-name-link') else "N/A"
                
                rating_tag = item.find('span', class_='rating-other-user-rating')
                rating = rating_tag.span.text.strip() if rating_tag else "N/A"
                
                date = item.find('span', class_='review-date').text.strip() if item.find('span', class_='review-date') else "N/A"
                
                title = item.find('a', class_='title').text.strip() if item.find('a', class_='title') else "N/A"
                
                review_text = item.find('div', class_='text').text.strip() if item.find('div', class_='text') else "N/A"

                rezension = {
                    "data-review-id": data_review_id,
                    "username": username,
                    "rating": rating,
                    "date": date,
                    "title": title,
                    "text": review_text
                }
                rezensionen.append(rezension)
    return rezensionen    

for subdir, dirs, files in os.walk(quell_verzeichnis):
    print(f"Bearbeite Verzeichnis {subdir}")
    # Extrahiere IMDb-ID
    imdb_id_match = re.search(r'tt\d+', subdir)
    if imdb_id_match:
        imdb_id = imdb_id_match.group()

        for file in files:
            if file.endswith('.htm'):
                file_path = os.path.join(subdir, file)
                print(f"HTML-Datei auslesen: {file_path}")
                
                titel, jahr, sumrez = extract_titel_jahr(file_path)
                rezensionen = extract_rezensionen(file_path)
                
                if imdb_id not in filme_daten:
                    filme_daten[imdb_id] = {
                        "titel": titel,  
                        "jahr": jahr,   
                        "Anzahl Rezessionen":sumrez, 
                        "rezensionen": rezensionen
                    }
                else:
                    filme_daten[imdb_id]["rezensionen"].extend(rezensionen)
               

# JSON-Datei schreiben
with open(json_dateipfad, 'w', encoding='utf-8') as jsonfile:
    json.dump(filme_daten, jsonfile, ensure_ascii=False, indent=4)

print(f"Die Daten wurden in {json_dateipfad} gespeichert.")