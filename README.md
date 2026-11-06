# TravelTide – Kundenanalyse und Rewards-Programm

Das Projekt untersucht das Reise- und Buchungsverhalten einer vorgegebenen Nutzerkohorte. Aus der explorativen Datenanalyse entstehen Nutzerfeatures, K-Means- und Regelgruppen sowie vorsichtige Vorschläge für ein Rewards-Programm. Eine Zuordnung beschreibt eine **Arbeitshypothese**, keine gemessene Präferenz und keinen nachgewiesenen Marketingeffekt.

## Verbindlicher Ergebnisstand

- Referenzdatum: **16.07.2023, Tagesende UTC**, zentral in `config.py` definiert.
- Unveränderte ursprüngliche Kohorte: **5.998 Nutzer**.
- Beobachtungsfenster bis zum Referenzdatum: **48.587 Sessions** und **15.851 unterschiedliche beobachtete gebuchte Reisen**.
- **486 Nutzer** haben bis zu diesem früheren Stichtag noch nicht mehr als sieben Sessions. Die Kohorte wird bewusst nicht neu ausgewählt.
- Explorative Arbeitslösung: **K-Means mit k=3**; k=2 bis 5 und unabhängige Regelgruppen werden verglichen.
- **171 robuste Perk-Arbeitshypothesen**: 128 erste Hotelnacht kostenlos, 38 kostenloses Gepäck, 5 exklusive Rabatte.
- **5.827 Nutzer** erhalten eine allgemeine Einladung beziehungsweise einen Beobachtungs- oder Testauftrag. Für kostenlose Mahlzeiten fehlt direkte Evidenz; für kostenlose Stornierung entsteht unter den strengen Regeln kein robuster finaler Vorschlag.

## Ordner und Dateien

| Pfad | Zweck |
|---|---|
| `01_EDA.ipynb` | Rohdatenqualität, Aufbereitung, EDA und Session-Level-Datensatz |
| `02_Features_mit_Segmentierung.ipynb` | Nutzerfeatures, Hypothesen, Feature-Auswahl, k-Vergleich, Regeln und Sensitivität |
| `03_Dips_Diagnose.ipynb` | Ungefilterte SQL-Aggregate zur Diagnose der Datenbrüche; Kohorte nur als grafischer Vergleich |
| `04_Stichtag_Vergleich.ipynb` | Vergleich des ursprünglichen Datenendes mit dem finalen Stichtag bei gleicher Kohorte |
| `05_Abschluss.ipynb` | Verbindliche Gruppenprofile, finale Nutzerentscheidungen und Erfolgsmessung |
| `config.py` | Gemeinsame Pfade, SQL-Parameter, Farben und finaler Stichtag |
| `eda_functions.py` | Wiederverwendbare Anzeige- und Prüffunktionen |
| `Sessions.sql`, `Flights.sql`, `Users.sql`, `Hotels.sql` | Einzelabfragen für die ursprüngliche Kohorte |
| `Data.sql` | Alternative SQL-Sammlung; kein automatischer Verarbeitungsschritt |
| `src/02_Features_Baseline.ipynb` | Eingefrorene Rechenquelle für Notebook 04; nicht zusätzlich manuell ausführen |
| `data/` | Lokale Eingaben, Zwischenstände und finale CSVs; nicht in Git enthalten |
| `Abgabe/` | Abschlussdokumente; siehe unten |

`backups/`, `PowerBI/` und `Tableau/` gehören nicht zum hier dokumentierten Analyseablauf.

## Installation

Geprüfte Umgebung: **Python 3.14.6**. Die verwendeten Analysepakete sind in `requirements.txt` festgelegt; der dokumentierte Abschlusslauf steht zusätzlich in `Abgabe/runtime_versions.json`. Die requirements ergänzen den Notebook-Kernel. PostgreSQL verwendet den Import `psycopg2`; für die Installation wird `psycopg2-binary` verwendet. Beide Distributionen nicht gleichzeitig installieren.

Im Projektordner unter Windows:

```powershell
py -3.14 -m venv venv
.env\Scripts\python.exe -m pip install -r requirements.txt
```

In VS Code die Python- und Jupyter-Erweiterung verwenden, dann `venv` als Notebook-Kernel auswählen. Vor einem vollständigen Lauf den Kernel neu starten und die Zellen von oben nach unten ausführen. Notebook 01 und 02 enthalten zusätzlich eine Paketprüfung; die Installation über requirements ist der vorgesehene reproduzierbare Weg.

## Lokale Daten und Ausführung

**Ein Git-Klon allein ist nicht ausführbar:** `data/` und `secrets.json` bleiben absichtlich lokal. Die folgenden Eingaben aus dem finalen Datenordner müssen separat bereitgestellt werden:

- `data/Sessions.csv`, `Flights.csv`, `Users.csv`, `Hotels.csv` für Notebook 01.
- `data/data_preprocessing/`: `sessions_analysis.csv`, `flights_analysis.csv`, `users_analysis.csv`, `hotels_analysis.csv` und `session_level_analysis.csv` für Notebook 02 und 04.
- `data/dip_analysis/`: `all_weekly.csv`, `cohort_weekly.csv`, `daily_end_of_data.csv`, `april_user_flows.csv` und `april_context.csv` für Notebook 03.

Mit den vorhandenen CSVs sind keine Datenbankzugangsdaten nötig. Die Notebooks werden in der Reihenfolge **01 → 02 → 03 → 04 → 05** ausgeführt. Notebook 03 ist diagnostisch unabhängig. Notebook 04 rechnet beide Szenarien aus der eingefrorenen Baseline; Notebook 05 benötigt dessen Vergleichsexporte.

Notebook 01 liest standardmäßig vorhandene Rohdaten und überschreibt keine aufbereiteten CSVs: `RUN_DATABASE_EXPORT=False` und `RUN_PREPROCESSING_EXPORT=False`. Notebook 02, 04 und 05 schreiben ihre jeweiligen Ergebnisdateien bei der Ausführung neu.

Bei einem bewussten Neuaufbau der Aufbereitung `RUN_PREPROCESSING_EXPORT=True` in 01 setzen und danach 02, 04 und 05 neu berechnen. Notebook 05 prüft die Quellen von 04 mit SHA-256 und stoppt bei abweichenden Eingaben. Nach Änderungen an Feature-Formeln muss die eingefrorene Baseline bewusst überprüft und versioniert werden; Änderungen in 02 werden nicht automatisch von 04 übernommen.

Notebook 03 liest mitgelieferte Aggregate. Die vollständigen SQL-Abfragen zu deren Neuerstellung sind im aktuellen Projekt nicht enthalten; die vier Kohortenabfragen ersetzen diese ungefilterten Diagnoseabfragen nicht.

## Optionaler Datenbankabruf

Eine lokale, nicht versionierte `secrets.json` neben `config.py` enthält:

```json
{
  "db_user": "DEIN_BENUTZERNAME",
  "db_password": "DEIN_PASSWORT"
}
```

`RUN_DATABASE_EXPORT=True` in Notebook 01 aktiviert den Abruf. **Vorhandene Roh-CSVs werden übersprungen**; für einen Neuabruf die betreffenden Dateien vorher bewusst sichern und aus dem Eingabepfad verschieben. Die ursprüngliche Kohorte basiert auf mehr als sieben Sessions ab `SESSION_START` (einschließlich), wie in `config.py` vorgegeben. Der spätere finale Analysestichtag ist davon getrennt.

## Ergebnisdateien

| Pfad | Inhalt |
|---|---|
| `data/data_features/working_cutoff_20230716/` | Arbeitsfeatures, Qualitätsberichte und Segmentierung aus Notebook 02 |
| `data/data_features/cutoff_comparison_20230716/` | Vergleichsexporte und Quellenprüfsummen aus Notebook 04 |
| `data/data_features/final/users_final.csv` | Finale Nutzerfeatures, Segment und Entscheidungen |
| `data/data_features/final/user_perk_actions.csv` | Eine Zeile je Nutzer mit Kommunikationsvariante, Begründung, Evidenz und nächster Aktion |
| `data/data_features/final/segment_profiles.csv` | Gruppenmediane; zugehörige Fallzahlen in `segment_profile_observations.csv` |
| `data/data_features/final/release_manifest.json` | Referenzdatum, Population, Methodik und Quellprüfsummen |
| `data/data_features/final/data_dictionary.csv` | Mitgeliefertes Datenwörterbuch; wird von Notebook 05 nicht neu erzeugt |

Ältere Dateien direkt in `data/data_features/` sowie `segmentation/` und `priorities_1_4/` sind Entwicklungs- beziehungsweise Vergleichsstände. **Verbindlich ist `data/data_features/final/`.** Die zusätzliche Datei `data/session_level_analysis.csv` ist nicht der Eingabepfad für Notebook 02; maßgeblich ist die Datei unter `data/data_preprocessing/`.

Vorhandene Abschlussdokumente:

- `Abgabe/TravelTide_-_Praesentation_Rewards_Programm.pptx`
- `Abgabe/TravelTide_Executive_Onepager.docx`
- `Abgabe/TravelTide_Executive_Summary.docx`
- `Abgabe/TravelTide_QA_Cheat_Sheet.docx`
- `Abgabe/Erfolgsmessung.md`
- `Abgabe/runtime_versions.json`

Diese Dokumente lassen sich unabhängig von den Notebooks öffnen. Ihre Erstellung ist kein automatischer Schritt der fünf Notebooks. ZIP-Pakete und BI-Dateien bleiben von Git ausgeschlossen; Abgabedokumente und die erforderliche Baseline in `src/` werden zugelassen.

## Zählweisen und Grenzen

Sessions: eine Zeile je `session_id`. Reisen: verschiedene `trip_id` mit beobachtetem Buchungsflag. Flug und Hotel derselben Reise zählen als zwei Komponenten, aber nur eine Reise. Eine vorhandene `trip_id` allein beweist keine Buchung. Beobachtete Stornos werden nicht pauschal aus der Historie entfernt. Unbekannte Quoten sind nicht null.

Negative Nächte und Check-out vor Check-in werden untersucht und aus Dauer- beziehungsweise berechneten Gesamtkostenkennzahlen ausgeschlossen, nicht durch Absolutwerte korrigiert. Modell-Imputation und Ausreißerbegrenzung verändern nur die Modellmatrix. Der Flug-Basispreis wird vorläufig als Gesamtpreis vor Rabatt interpretiert; Hotelpreise gelten pro Zimmer und Nacht. Rückflugumfang und Teilstornos sind nicht abschließend auflösbar.

Ab 21.07.2023 fehlen in den vorliegenden ungefilterten Daten Sessions ohne Buchung. Datenlieferung oder Erzeugungslogik sind plausible, nicht bewiesene Ursachen. Der April-Dip betrifft vor allem bekannte Nutzer; Kampagneneffekte und Saisonalität bleiben Hypothesen. Preise und Stammdaten sind nicht historisch versioniert. Die ursprüngliche Kohortenauswahl begrenzt die Übertragbarkeit. Die Perk-Regeln sind kein gelerntes oder kausal bestätigtes Präferenzmodell.

## Quellen

- Masterschool: DS Mastery Project, Woche 1–4, einschließlich der Projektvorgaben.
- Vergleichsprojekt: https://github.com/anuarsantoyo/TravelTideOct26
- Methodik: https://scikit-learn.org/stable/modules/clustering.html

Die Referenz wurde kritisch geprüft; automatische Nachtkorrekturen, vervielfachende Joins und überschreibende Gruppenregeln wurden nicht übernommen.
