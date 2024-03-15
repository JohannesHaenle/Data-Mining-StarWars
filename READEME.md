# Sentiment Analyse IAMDB Rezessionen (Scraping, Cleaning, VADER/Textblob/Roberta, Analyse)

## Explorative Sentimentanalyse für die Rezensionnen der Star Wars Filme aus der IAMDB Datenbank (mittlerweile Amazon)

Das Projekt wurde ausschließlich mittels Python durchgeführt und es wird eine Umgebung mit den in der Ausarbeitung genannten Bibliotheken benötigt

* Download der erfoderlichen Pakete / Bibliotheken (Empfohlen mit Pip) oder Erstellen einer venv mittels "textmining_env.yml"

* Durchführung Scraping:
    *
    *
    *

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
        





