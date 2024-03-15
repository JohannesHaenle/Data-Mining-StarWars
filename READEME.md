# Sentiment Analyse IAMDB Rezessionen (Scraping, Cleaning, VADER/Textblob/Roberta, Analyse)

## Explorative Sentimentanalyse für die Rezensionnen der Star Wars Filme aus der IAMDB Datenbank (mittlerweile Amazon)

Das Projekt wurde ausschließlich mittels Python durchgeführt und es wird eine Umgebung mit den in der Ausarbeitung genannten Bibliotheken benötigt

* Download der erfoderlichen Pakete / Bibliotheken (Empfohlen mit Pip) oder Erstellen einer venv mittels "textmining_env.yml"

* Durchführung Scraping:
    * Stellen Sie sicher, dass Python auf Ihrem System installiert ist. Diese Skripte wurden mit Python 3.8 und neuer getestet.
    * Benötigte Bibliotheken
        * BeautifulSoup: Für das Parsen der HTML-Inhalte.   -> pip install beautifulsoup4
        * Requests: Zum Senden von HTTP-Anfragen an IMDb.   -> pip install requests
        * Selenium: Für das Interagieren mit Webseiten, insbesondere zum Klicken auf Buttons, die nicht durch einfache HTTP-Anfragen ausgelöst werden können. -> pip install selenium
    * WebDriver
      
      Für Selenium benötigen Sie einen WebDriver für den Browser, den Sie verwenden möchten. In den Skripten wird Firefox und dessen geckodriver verwendet.

      Installation des WebDrivers
      
      Laden Sie den geckodriver für Firefox von der offiziellen GitHub-Seite (https://github.com/mozilla/geckodriver/releases) herunter und extrahieren Sie die ausführbare Datei in einen Ordner, der in Ihrem System-PATH enthalten ist, oder passen Sie den Pfad im Skript entsprechend an.
    * Ausführung der Skripte
        * Auslesen der Pfade zu den gewünschten Filmen: Nutzen Sie das erste Skript 01_scrape_getIMDBMovieUrls.py, um Film-URLs von IMDb zu sammeln und in einer Textdatei abzuspeichern.
        * Anlegen lokaler Kopien: Verwenden Sie das zweite Skript 02_scrape_getMoviePageCopy.py, um lokale Kopien der IMDb-Seiten basierend auf den gesammelten URLs zu erstellen.
        * Auslesen der Film informationen: Mit dem dritten Skript 03_scrape_scrapeMovieInfos.py werden Informationen aus den lokalen Kopien extrahiert und in einer JSON-Datei zusammengefasst.
        * Erweitern des JSON um weitere Informationen: Das vierte Skript 04_scrape_extendMovieInfos.py erweitert die JSON-Datei um zusätzliche Informationen, die durch erneutes Scraping von IMDb erhalten werden.
          
      Stellen Sie sicher, dass Sie in den Skripte die verwendeten Dateibezeichnungen und URL korrekt angepasst haben und führen Sie diese in der oben beschriebenen Reihenfolge aus, um die notwendigen Daten schrittweise zu sammeln und zu verarbeiten.
  * Hinweise
     * Passen Sie die Pfade in den Skripten entsprechend Ihrem System und Ihren Anforderungen an.
     * Nutzungsbedingungen und Richtlinien von IMDb beachten, bezüglich des Scrapings und des Umgangs mit den Daten.
     * Berücksitigen Sie ethische Richtlinien und Datenschutzbestimmungen.

* Datenaufbereitung und Überführung in Pandas Dataframe für Ausgangsbasis der Analyse & Modellanwendung
    * Ausführung des .ipynb Notebooks
        * Überführung der rohen Rezensionsdaten aus "filme_rezensionen_extendet.json" in Pandas Dataframe
        * Data Cleaning
        * Explorative Deskriptive Statistik
        * Sentiment Analyse (Beschreibung in Markdown)
            * Textblob: Tokenisierung / Entfernung Stopwords / Anwendung Model auf Rezensionen
            * VADER: Anwedung des Modells
            * Roberta: Anwedung des Modells --> ggf. auf GPU laufen lassen / Ressourcenintensiv
        * Merging der Datensätze --> Komprimierung in .pckl File
        * Erstellung Wordclouds
    
    * Analyse.ipynb Notebook
        * Durchführung verschiedener Analysen
        * Klassifizierung / Performance Berechnung
        * Plotting verschiedener Ergebnise
        





