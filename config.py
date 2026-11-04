import json
from pathlib import Path
from urllib.parse import quote

SESSION_START = "2023-01-04"
SESSION_COUNTER = 7

FOLDER = Path(__file__).parent
DATA_FOLDER = FOLDER / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
DATA_PREPROCESSING_FOLDER = DATA_FOLDER / "data_preprocessing"
DATA_PREPROCESSING_FOLDER.mkdir(parents=True, exist_ok=True)

SESSIONS_SQL = (FOLDER / "Sessions.sql").read_text(encoding="utf-8")
FLIGHTS_SQL = (FOLDER / "Flights.sql").read_text(encoding="utf-8")
USERS_SQL = (FOLDER / "Users.sql").read_text(encoding="utf-8")
HOTELS_SQL = (FOLDER / "Hotels.sql").read_text(encoding="utf-8")

QUERIES = {
    "Sessions": {"sql": SESSIONS_SQL, "csv": DATA_FOLDER / "Sessions.csv"},
    "Flights": {"sql": FLIGHTS_SQL, "csv": DATA_FOLDER / "Flights.csv"},
    "Users": {"sql": USERS_SQL, "csv": DATA_FOLDER / "Users.csv"},
    "Hotels": {"sql": HOTELS_SQL, "csv": DATA_FOLDER / "Hotels.csv"},
}

PARAMS = {
    "session_start": SESSION_START,
    "session_counter": SESSION_COUNTER,
}

secrets_path = Path(__file__).with_name("secrets.json")

# CSV-basierte Analyse funktioniert auch ohne Datenbank-Zugangsdaten.
DATABASE_URL = None
if secrets_path.is_file():
    with secrets_path.open(encoding="utf-8") as file:
        credentials = json.load(file)
    
    
    DATABASE_URL = (
        f"postgresql://{quote(credentials['db_user'], safe='')}:"
        f"{quote(credentials['db_password'], safe='')}@"
        "ep-noisy-flower-846766.us-east-2.aws.neon.tech/"
        "TravelTide?sslmode=require"
    )

# --- TravelTide Theme & UI Colors -----------------------------------------
THEME = {
    # Hauptfarben
    "primary":         "#006D77",  # Ozean-Petrol
    "secondary":       "#00B4D8",  # Klares Wasserblau
    "accent":          "#FFB703",  # Sonnengelb für Highlights

    # Hintergründe und Text
    "background":      "#F4FAFC",  # Kühler, heller Hintergrund
    "surface":         "#FFFFFF",  # Karten und Tabellen
    "surface_alt":     "#E6F4F5",  # Dezentes Türkis
    "sand":            "#FFF4E0",  # Warmer Sandton
    "text":            "#17324D",  # Dunkles Marineblau
    "text_muted":      "#526B7A",  # Gedämpfter Begleittext
    "border":          "#D5E5EB",

    # Statusfarben im Urlaubslook
    "success_bg":      "#EAF8F7",  # Helles Lagunenwasser
    "success_border":  "#168B8A",  # Kräftiges Meerestürkis
    "danger_bg":       "#FFF1EB",  # Zarter Pfirsich / Muschelton
    "danger_border":   "#D8644B",  # Warme Koralle

    # Diagramme
    "palette":         "crest",
    "chart_colors": [
        "#006D77",
        "#00B4D8",
        "#83C5BE",
        "#FFB703",
        "#17324D",
        "#E29578",
    ],
}

# --- Farben für TravelTide Perks / Kundensegmente ------------------------
PERK_COLORS = {
    "Free Cancellation":    "#1d4ed8",  # Primärblau (Fokus-Perk)
    "Free Baggage":         "#0ea5e9",  # Ozean-Cyan
    "Complimentary Meals":  "#f59e0b",  # Warmes Amber (Kontrast für Kulinarik)
    "First Night Free":     "#10b981",  # Frisches Mint/Grün (Hotel-Vorteil)
    "Member Discounts":     "#8b5cf6",  # Edles Violett (Exklusivität)
}

perk_order = list(PERK_COLORS.keys())

WIDTH = 1200
# Ausgabeordner fuer 02_Features
DATA_FEATURES_FOLDER = DATA_FOLDER / "data_features"

# Verbindlicher Abschlussstand; ursprüngliche Kohorte bleibt erhalten.
ANALYSIS_REFERENCE_DATE = "2023-07-16T23:59:59.999999Z"
FINAL_DATA_FOLDER = DATA_FEATURES_FOLDER / "final"
BASELINE_FEATURE_NOTEBOOK = FOLDER / "src" / "02_Features_Baseline.ipynb"
