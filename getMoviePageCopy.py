import os
import re
import random
import time

import random
from bs4 import BeautifulSoup

from datetime import datetime
from selenium import webdriver # Install before -> pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# Pfade für Ein/Ausgabe
script_path = os.path.dirname(os.path.realpath(__file__))
export_path = os.path.join(script_path, "exportFullHtml")
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"

geckodriver_path = os.path.join(script_path,'geckodriver.exe')
if not os.path.exists(geckodriver_path):
    raise Exception(f"geckodriver wurde nicht im Pfad gefunden: {geckodriver_path}")

firefox_options = Options()
firefox_options.binary_location = firefox_binary_path
service = Service(executable_path=geckodriver_path)
selenium_driver = webdriver.Firefox(service=service, options=firefox_options)

# aktuelle Zeit im Format "Jahr-Monat-Tag_Stunde-Minute-Sekunde" 
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

def get_random_wait_time():
    """
    Gibt eine zufällige Wartezeit zurück, um zwischen 5 und 9 Sekunden zu warten. Wird beim Nachladen der Kommentare verwendet um eine natürliche Userinteraktion zu simulieren.

    :return: Eine zufällig generierte Wartezeit in Sekunden (int).
    """
    return random.randint(5, 9)


def clean_string(in_string):
    """
    Bereinigt einen Eingabestring, indem alle unerwünschten Zeichen entfernt werden, die keine Buchstaben (Groß- und Kleinbuchstaben), Zahlen oder Leerzeichen sind. Wird verwendet um den String zu bereinigen, bevor ein Verzeichnis angelegt wird.

    :param in_string: Der zu bereinigende Eingabestring (str).
    :return: Der bereinigte String (str).
    """
    clean_string= re.sub(r'[^a-zA-Z0-9 ]', '', in_string)
    return clean_string    
    

def create_folder(base_path, title, imdb_film_id):
    """
    Erstellt ein Verzeichnis für den übergebenen Film basierend auf dessen Titel und der IMDb-Film-ID.

    :param base_path: Der Basispfad, in dem das Verzeichnis erstellt werden soll (str).
    :param title: Der Titel des Films (str).
    :param imdb_film_id: Die IMDb-ID des Films (str).
    :return: Der Pfad zum erstellten Verzeichnis (str).
    """
    clean_title = clean_string(title[:150])  # Titel auf 150 Zeichen begrenzen 
    targetname = f"{clean_title}_{imdb_film_id}"
    folder_path = os.path.join(base_path, targetname)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def scrape_imdb(url, base_path):
    
    print(f"Using URL {url}")
    selenium_driver.get(url)
    
    #sortierungsart ermitteln 
    sort_match = re.search(r"sort=([^&]+)", url)
    dir_match = re.search(r"dir=([^&]+)", url)
    
    sort_value = sort_match.group(1) if sort_match else 'xxx'
    dir_value = dir_match.group(1) if dir_match else 'xxx'

    match = re.search(r'/title/(tt\d+)/', url)
    if match:
        imdb_film_id = match.group(1)
    
    #Cookie banner abwarten und ablehnen  
    try:
        decline_button = WebDriverWait(selenium_driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="reject-button"]'))
        )
        decline_button.click()
    except Exception as e:
        print(f"Fehler beim CookieBanner: {e}")
    
    
    #Rezessionen nachladen - solange bis es keinen load More Button gibt
    while True:
        try:
            # Warten bis auf den "Load More"-Button, geklickt wird in einer zufälligen Zeit
            load_more_button = WebDriverWait(selenium_driver, get_random_wait_time()).until(
                EC.element_to_be_clickable((By.ID, "load-more-trigger"))
            )
            # Scrollen zum "Load More"-Button,
            selenium_driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            # Klicken auf den "Load More"-Button
            selenium_driver.execute_script("arguments[0].click();", load_more_button)
            
            # Optional: Warte einen Moment, damit die Seite nach dem Klicken des Buttons laden kann
            time.sleep(get_random_wait_time())

        except TimeoutException:
            # Wenn der "Load More"-Button nicht gefunden wird (sinngemäß keine weiteren Inhalte zum Laden)
            print("Load more button not found, stopping...")
            break

    fullHtml = selenium_driver.page_source
    soup = BeautifulSoup(fullHtml, 'html.parser')

    # Titel auslesen
    meta_title = soup.find('meta', property='og:title') or soup.find('meta', name='title')
    title = meta_title['content'] if meta_title else 'TitelNotFound(dbg)'
    print(f"working on Titel: {title}")
    
    moviePath = create_folder(export_path, title, imdb_film_id)
    
    with open(os.path.join(moviePath, f"{current_time }_SORT_{sort_value}_DIR_{dir_value}.htm"), 'w', encoding='utf-8') as file:
        file.write(fullHtml)
    
    print(f"ready URL {url}")

def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

#URL der IMDB Seite - Filter Hide Spoilers deaktivieren -> Spoiler sollen angezeigt werden!! &ratingFilter=0
#  Übergabeparameter  für künftige linkanpassung -> ?spoiler=hide&sort=curated&dir=desc&ratingFilter=0
#scrape_imdb('https://www.imdb.com/title/tt1517268/reviews?spoiler=hide&sort=curated&dir=desc&ratingFilter=0', script_path)

#lesen der ZielUrls aus textdatei und ermitteln der Informationen
#url_filename= 'imdb_movie_urls.txt'
#url_filename= 'imdb_movie_urlsMostRated.txt'
url_filename= 'StarWarsUrlsSingle.txt'
urls = read_urls_from_file(os.path.join(script_path,url_filename))

for url in urls:
    scrape_imdb(url, export_path)

selenium_driver.quit()   
print("all Done")