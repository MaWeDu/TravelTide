# TravelTide - Kundenanalyse und Rewards-Programm

## Ergebnis und verbindliche Entscheidungen
Stichtag: **16.07.2023, Tagesende UTC**. Die ursprüngliche Kohorte bleibt mit 5.998 Nutzern
erhalten. Das Beobachtungsfenster enthält 48.587 Sessions und 15.851 unterschiedliche
beobachtete gebuchte Reisen. 486 Nutzer erfüllen bis zum früheren Stichtag die ursprüngliche
Grenze von mehr als sieben Sessions noch nicht. Dies ist bewusst keine Neuauswahl.

K-Means mit k=3 liefert die explorativen Arbeitsgruppen. Die Regelgruppen bleiben ein
erklärbarer Vergleich. Die vollständige Nutzerdatei enthält für 171 Nutzer eine über alle
geprüften Annahmevarianten stabile Perk-Arbeitshypothese. 5.827 Nutzer erhalten eine allgemeine
Einladung bzw. einen Beobachtungs-/Testauftrag. Das sind keine behaupteten fehlenden Präferenzen.
Für Mahlzeiten fehlt direkte Evidenz; für Stornierung entsteht unter den strengen Regeln
keine robuste finale Empfehlung. Das Projekt bestätigt die fünf Perk-Hypothesen deshalb nur teilweise.

## Dateien und Reihenfolge
1. `01_EDA.ipynb`: ursprüngliche Rohdaten, Qualitätsprüfung und Aufbereitung. Der ursprüngliche Zeitraum bleibt für die Diagnose erhalten. Datenbankabruf und CSV-Neuexport sind standardmäßig ausgeschaltet.
2. `02_Features_mit_Segmentierung.ipynb`: Feature Engineering und Segmentierung mit dem finalen Stichtag aus `config.py`. Zusätzliche SQL-Versuchszellen wurden entfernt; deren Original liegt in der Sicherung.
3. `03_Dips_Diagnose.ipynb`: ungefilterte SQL-Aggregate und rein grafischer Kohortenvergleich aus `data/dip_analysis`.
4. `04_Stichtag_Vergleich.ipynb`: bisheriges Datenende gegenüber 16.07.; nutzt die eingefrorene `src/02_Features_Baseline.ipynb`, damit die Vergleichsbasis erhalten bleibt.
5. `05_Abschluss.ipynb`: verbindliche Gruppenprofile, Nutzerdatei und Erfolgsmessung. Verwendet die geprüften Vergleichsexporte und prüft ihre Quellen anhand von SHA-256.

`config.py` ist die einzige Konfiguration für Pfade, Farben und Stichtag. `eda_functions.py`
enthält die Anzeige-/Prüffunktionen. `src/02_Features_Baseline.ipynb` ist eine eingefrorene
Rechenquelle für Notebook 04, kein zusätzlicher Bearbeitungsschritt.

## Ausführen
Python-Umgebung in VS Code/Jupyter auswählen und die getesteten Paketversionen aus `requirements.txt` installieren. Die geprüfte Python-Version steht in `Abgabe/runtime_versions.json`.
Notebooks im Projektordner öffnen. Für die mitgelieferten CSV-Daten sind keine Zugangsdaten nötig.
Die finalen Tabellen und PDFs können ohne Ausführung direkt gelesen werden.
Bei Änderungen an Quell-CSVs zuerst 01 mit `RUN_PREPROCESSING_EXPORT=True` ausführen, danach 02 und 04 neu berechnen, dann 05. Die Prüfsummen in 05
verhindern eine unbemerkte Verwendung veralteter Vergleichsergebnisse. Nach einer Änderung der
Feature-Formeln muss die eingefrorene Vergleichsbasis bewusst neu versioniert werden.

Ein optionaler Neuabruf aus der Datenbank erfordert eine lokale `secrets.json` mit den Schlüsseln
`db_user` und `db_password` und `RUN_DATABASE_EXPORT=True` in Notebook 01. Zugangsdaten sind
nicht Bestandteil des Abgabepakets. Vorhandene Quell-CSVs werden wie dokumentiert übersprungen;
ein Neuabruf ist daher eine bewusst getrennte Aktualisierung.

## Verbindliche Ausgaben
- `data/data_features/final/users_final.csv`: alle Nutzerfeatures, Segment und Entscheidungen.
- `data/data_features/final/user_perk_actions.csv`: eine Zeile je Nutzer mit Vorteil (falls robust), Kommunikationsvariante, Begründung, Evidenz und nächster Aktion.
- `data/data_features/final/segment_profiles.csv` und `segment_profile_observations.csv`: Mediane und zugehörige Fallzahlen.
- `data/data_features/final/release_manifest.json`: Stichtag, Population, Methodik und Quellprüfsummen.
- `Abgabe/TravelTide_Bericht.pdf`: eine Seite Executive Summary plus drei Seiten Bericht.
- `Abgabe/TravelTide_Praesentation.pptx`: sechs Folien mit editierbaren Diagrammen und Sprechernotizen.
- `Abgabe/Erfolgsmessung.md`: kontrollierter Test und noch zu erhebende Planungsdaten.

## Zählweisen
Sessions: eine Zeile je `session_id`. Reisen: verschiedene `trip_id` mit beobachtetem Buchungsflag.
Flug und Hotel derselben Reise zählen als zwei Komponenten, aber nur eine Reise. Stornos werden
beobachtungsbezogen gezählt und nicht pauschal aus der Historie entfernt. Unbekannte Quoten sind
nicht null. Modell-Imputation und Begrenzung extremer Werte verändern ausschließlich die Modellmatrix.
Die Preisinterpretation für Flug-Gesamtpreise vor Rabatt bleibt vorläufig; Hotelpreise gelten pro
Zimmer und Nacht. Der Umfang von Rückflug und Teilstornos ist nicht abschließend auflösbar.

## Grenzen
Ab 21.07.2023 fehlen in der ungefilterten Datenbank Sessions ohne Buchung. Datenlieferung oder
Erzeugungslogik sind plausible Ursachen, aber nicht bewiesen. Der April-Dip betrifft vor allem
bekannte Nutzer; Kampagneneffekte und Saisonalität bleiben Hypothesen. Preise und Stammdaten
sind nicht historisch versioniert. Keine der Perk-Regeln ist ein gelerntes oder kausal bestätigtes
Präferenzmodell. Die ursprüngliche Kohortenauswahl begrenzt die Übertragbarkeit.

## Quellen
Masterschool: DS Mastery Project, Woche 1-4, einschließlich Abgabeinformationen 2026.
Referenz: https://github.com/anuarsantoyo/TravelTideOct26
Methodik: https://scikit-learn.org/stable/modules/clustering.html
Die Referenz wurde kritisch geprüft; Nachtkorrektur, vervielfachende Joins und überschreibende
Gruppenregeln wurden nicht übernommen. Datenstand und Annahmen sind in den Notebooks dokumentiert.

## Versionshinweis
Frühere Feature-CSV-Dateien im allgemeinen `data_features`-Ordner sind Entwicklungsstände. Verbindlich sind die Dateien in `data_features/final`.
