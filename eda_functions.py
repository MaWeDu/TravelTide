"""EDA-Hilfsfunktionen fuer TravelTide-Notebooks.

Benutzung
---------
    import eda_functions as eda
    tables = eda.load_tables(config.QUERIES)
    eda.preview_tables(tables, config.THEME)
    overview = eda.column_overview(tables["Sessions"])
    eda.display_table(overview, title="Sessions: Datenqualitaet")

Voraussetzungen: pandas, numpy, IPython und jinja2 (pandas Styler).
Installation im Notebook: %pip install pandas numpy ipython jinja2

Die Funktionen laden oder untersuchen Daten, bereinigen sie aber nicht.
Alle check_*-Funktionen liefern (Bericht, betroffene Originalzeilen).
Fehlende Werte werden separat gezaehlt; sie sind keine Typabweichungen.
Typen werden aus Inhalten abgeleitet: eine Zahl als Text gilt als Zahl.
Datumsstrings: ISO-Format YYYY-MM-DD mit optionaler Uhrzeit.
Vor errors="coerce" pruefen: Konvertierung kann Originalfehler verdecken.
"""

import re
from datetime import date, datetime
from numbers import Number

import numpy as np
import pandas as pd
from IPython.display import HTML, display


def detect_value_type(value):
    """Erkennt den Inhaltstyp eines einzelnen skalaren Wertes.

    Args:
        value: Einzelner Zellwert, keine Liste oder Series.

    Returns:
        Text, Zahl, Datum, Boolean, Leertext, Ungueltiges Datum (deutsch
        beschriftet) oder None fuer fehlende Werte. Andere Objekte werden
        mit ihrem Python-Typnamen bezeichnet.

    Beispiele:
        detect_value_type("2023-01-04") -> "Datum"
        detect_value_type("42") -> "Zahl"

    Numerische IDs werden als Zahl erkannt. Diese Erkennung beurteilt
    weder die fachliche Bedeutung noch die Gueltigkeit einer ID.
    """
    if pd.isna(value):
        return None

    if isinstance(value, (bool, np.bool_)):
        return "Boolean"

    if isinstance(value, (datetime, date, pd.Timestamp, np.datetime64)):
        return "Datum"

    if isinstance(value, Number):
        return "Zahl"

    if isinstance(value, str):
        text = value.strip()

        if not text:
            return "Leertext"

        if text.lower() in {"true", "false"}:
            return "Boolean"

        if re.fullmatch(
            r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
            text,
        ):
            return "Zahl"

        if re.match(r"^\d{4}-\d{2}-\d{2}(?:$|[ T])", text):
            try:
                pd.Timestamp(text)
                return "Datum"
            except (ValueError, TypeError, OverflowError):
                return "Ungültiges Datum"

        return "Text"

    return type(value).__name__



from pathlib import Path
from html import escape


def column_overview(frame):
    """Berechnet ein Spaltenprofil mit gemeinsamem Qualitaetsstatus.

    Args:
        frame: DataFrame mit eindeutigen Spaltennamen und skalaren Zellen.

    Returns:
        DataFrame mit pandas-Datentyp, fehlenden Werten, Unique-Anzahl,
        Min/Max, haeufigstem Wert, Inhaltstyp und zusammengefasstem Status.

    Beispiel:
        overview = eda.column_overview(df_sessions)
        eda.display_table(overview, title="Sessions")

    Prozentanteile beziehen sich auf nicht fehlende Werte; Fehlend (%)
    bezieht sich auf alle Zeilen. Min/Max nur fuer einheitliche Zahlen
    oder Daten, ausser *_id. Datumsgrenzen werden in UTC dargestellt.
    Bei Gleichstand wird ein haeufigster Wert/Typ als Referenz gewaehlt.
    Typabweichungen vergleichen mit der Mehrheit, nicht mit einem Schema.
    Ungueltige Daten und Leertexte koennen zugleich Typabweichungen sein.
    """
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("frame muss ein pandas DataFrame sein.")
    if not frame.columns.is_unique:
        raise ValueError("Spaltennamen muessen eindeutig sein.")
    records = []
    
    for column in frame.columns:
        series = frame[column]
        valid = series.dropna()
    
        detected = series.map(detect_value_type)
        type_counts = detected.dropna().value_counts()
        value_counts = valid.value_counts()
    
        missing = int(series.isna().sum())
        invalid_dates = int(detected.eq("Ungültiges Datum").sum())
        blank_texts = int(detected.eq("Leertext").sum())
    
        dominant_type = "-"
        type_match = np.nan
        deviations = 0
        tied = False
    
        if not type_counts.empty:
            dominant_type = type_counts.index[0]
            type_match = 100 * type_counts.iloc[0] / type_counts.sum()
            deviations = int(type_counts.sum() - type_counts.iloc[0])
            tied = int(type_counts.eq(type_counts.iloc[0]).sum()) > 1
    
        # Min / Max für einheitliche Zahlen und Datumswerte, außer IDs
        minimum = maximum = "-"
        is_id = str(column).lower().endswith("_id")
    
        if not valid.empty and not deviations and not tied and not is_id:
            if dominant_type == "Zahl":
                numeric = pd.to_numeric(valid, errors="coerce")
                minimum, maximum = numeric.min(), numeric.max()
    
            elif dominant_type == "Datum":
                dates = pd.to_datetime(valid, utc=True, format="mixed")
                minimum, maximum = dates.min(), dates.max()
    
        # Gemeinsamer Status für fehlende Werte und Inhaltstypen
        messages = []
    
        if missing:
            messages.append("Fehlende Werte")
    
        if type_counts.empty:
            messages.append("Keine prüfbaren Werte")
        else:
            if tied:
                messages.append("Typ-Gleichstand")
            elif deviations:
                messages.append("Gemischte Inhaltstypen")
    
            if invalid_dates:
                messages.append("Ungültige Datumswerte")
    
            if blank_texts:
                messages.append("Leertexte")
    
        status = (
            "⚠️" + " · ".join(messages)
            if messages
            else "✅ Vollständig & einheitlich"
        )
    
        records.append({
            "Spalte": column,
            "Datentyp (pandas)": str(series.dtype),
            "Nicht fehlend": int(series.notna().sum()),
            "Fehlend": missing,
            "Fehlend (%)": (
                missing / len(series) * 100 if len(series) else np.nan
            ),
            "Eindeutige Werte": series.nunique(dropna=True),
            "Min": minimum,
            "Max": maximum,
            "Häufigster Wert": (
                str(value_counts.index[0])
                if not value_counts.empty else "-"
            ),
            "Häufigster Wert (%)": (
                value_counts.iloc[0] / len(valid) * 100
                if not value_counts.empty else np.nan
            ),
            "Häufigster Inhaltstyp": (
                f"{dominant_type} (Gleichstand)"
                if tied else dominant_type
            ),
            "Typübereinstimmung (%)": type_match,
            "Typabweichungen": deviations,
            "Ungültige Datumswerte": invalid_dates,
            "Leertexte": blank_texts,
            "Status": status,
        })
    
    
    column_info = pd.DataFrame(
        records,
        columns=[
            "Spalte",
            "Datentyp (pandas)",
            "Nicht fehlend",
            "Fehlend",
            "Fehlend (%)",
            "Eindeutige Werte",
            "Min",
            "Max",
            "Häufigster Wert",
            "Häufigster Wert (%)",
            "Häufigster Inhaltstyp",
            "Typübereinstimmung (%)",
            "Typabweichungen",
            "Ungültige Datumswerte",
            "Leertexte",
            "Status",
        ],
    ).set_index("Spalte")
    
    
    return column_info


def load_tables(queries, **read_csv_options):
    """Laedt CSV-Dateien aus einem QUERIES-Dictionary.

    Args:
        queries: {Name: {"csv": Dateipfad, ...}} wie in config.py.
        **read_csv_options: Optionen fuer pd.read_csv, z.B. sep=";".

    Returns:
        Dictionary {Name: DataFrame}. Keine Datenbankabfrage.

    Beispiel:
        tables = eda.load_tables(config.QUERIES)

    Fehlende/unlesbare Dateien erzeugen einen Fehler. Standardmaessig
    verwendet pandas seine Typ- und NA-Erkennung. Fuer strengere
    Rohdatenpruefung kann dtype="string" sinnvoll sein; Datentypen und
    fuehrende Nullen koennen sonst schon beim CSV-Lesen veraendert werden.
    """
    return {
        name: pd.read_csv(Path(query["csv"]), **read_csv_options)
        for name, query in queries.items()
    }


def _table_html(table):
    """Einheitliche kompakte Darstellung fuer alle Tabellen erzeugen."""
    formats = {c: "{:.2f}" for c in table.columns if str(c).endswith("(%)")}
    return (table.style
        .format(formats, na_rep="-", escape="html")
        .format_index(escape="html", axis=0)
        .format_index(escape="html", axis=1)
        .set_table_styles([
            {"selector": "th, td", "props": [
                ("white-space", "nowrap"), ("padding", "4px 10px"),
                ("font-size", "12px"), ("line-height", "18px"),
                ("vertical-align", "middle"), ("text-align", "left")
            ]},
            {"selector": "thead th", "props": [
                ("background", "#E6F4F5"), ("color", "#17324D")
            ]},
            {"selector": "tbody tr:nth-child(even)", "props": [
                ("background", "#F4FAFC")
            ]}
        ]).to_html())


def display_table(table, title=None, max_height=450, card_width=700):
    """Zeigt eine Tabelle in derselben Kartenbreite wie preview_tables.

    Args:
        table: DataFrame zur Anzeige.
        title: Optionale Ueberschrift.
        max_height: Maximale Hoehe des Tabellenbereichs in Pixeln.
        card_width: Aussenbreite der Karte; Standard 700 wie preview_tables.

    Beispiel:
        eda.display_table(overview, title="Sessions: Datenqualitaet")

    Lange Tabellen bleiben innerhalb der Karte horizontal scrollbar.
    Die Hoehe richtet sich bis max_height nach dem Inhalt.
    """
    height, width = max(100, int(max_height)), max(450, int(card_width))
    heading = (
        f'<h4 style="margin:0 0 10px;color:#006D77;">{escape(str(title))}</h4>'
        if title else ''
    )
    display(HTML(
        f'<section style="width:{width}px;max-width:100%;min-width:0;'
        'box-sizing:border-box;border:1px solid #D5E5EB;'
        'border-radius:8px;padding:12px;">'
        + heading
        + f'<div style="max-height:{height}px;overflow:auto;">'
        + _table_html(table)
        + '</div></section>'
    ))


def display_tables(tables, title=None, max_height=450, card_width=700):
    """Zeigt beliebige Ergebnistabellen nebeneinander statt untereinander.

    Args:
        tables: Dictionary {Ueberschrift: DataFrame}.
        title: Optionale gemeinsame Ueberschrift.
        max_height: Maximale Hoehe pro Tabelle in Pixeln.
        card_width: Breite jeder Tabellenkarte in Pixeln.

    Returns:
        None. Eine horizontale Reihe ohne Zeilenumbruch. Der aeussere
        Scrollbalken wechselt zwischen Karten; jede Tabelle ist bei Bedarf
        innerhalb ihrer Karte scrollbar. Lange Zellinhalte bleiben einzeilig.

    Beispiel:
        overviews = {name: eda.column_overview(frame)
                     for name, frame in tables.items()}
        eda.display_tables(overviews, title="Datenqualitaet")
    """
    if isinstance(tables, pd.DataFrame) or not hasattr(tables, "items"):
        raise TypeError('tables muss ein Dictionary {Name: DataFrame} sein.')
    if any(not isinstance(frame, pd.DataFrame) for frame in tables.values()):
        raise TypeError("Alle Werte muessen DataFrames sein.")
    height, width = max(100, int(max_height)), max(700, int(card_width))
    if title:
        display(HTML(f"<h4>{escape(str(title))}</h4>"))
    if not tables:
        display(HTML("<p>Keine Tabellen vorhanden.</p>"))
        return
    cards = []
    for name, frame in tables.items():
        cards.append(
            f'<section style="flex:0 0 {width}px;min-width:0;'
            'border:1px solid #D5E5EB;border-radius:8px;padding:12px;'
            'box-sizing:border-box;background:#FFFFFF;">'
            f'<h4 style="margin:0 0 10px;color:#006D77;">{escape(str(name))}</h4>'
            f'<div style="max-height:{height}px;overflow:auto;">'
            + _table_html(frame) + '</div></section>'
        )
    display(HTML(
        '<div style="display:flex;flex-wrap:nowrap;align-items:flex-start;'
        'gap:16px;overflow-x:auto;width:100%;padding-bottom:12px;">'
        + ''.join(cards) + '</div>'
    ))


def preview_tables(tables, theme, n=5, max_height=450, card_width=700):
    """Zeigt Tabellenvorschauen nebeneinander in einer horizontalen Reihe.

    Args:
        tables: Dictionary {Name: DataFrame}, kein einzelner DataFrame.
        theme: Farb-Dictionary aus config.THEME.
        n: Anzahl erster und letzter Zeilen; Ueberschneidungen erscheinen
            nur einmal. Eine Trennlinie markiert ausgelassene Zeilen.
        max_height: Maximale Hoehe einer Vorschau in Pixeln.
        card_width: Kartenbreite in Pixeln.

    Returns:
        None. Rohdaten werden nicht geaendert.

    Beispiele:
        eda.preview_tables(df, config.THEME)
        eda.preview_tables({"Sessions": df_sessions}, config.THEME, n=5)
    """
    if isinstance(tables, pd.DataFrame) or not hasattr(tables, "items"):
        raise TypeError('tables muss ein Dictionary sein, z.B. {"Sessions": df_sessions}.')
    if any(not isinstance(frame, pd.DataFrame) for frame in tables.values()):
        raise TypeError("Alle Werte muessen DataFrames sein.")
    if not isinstance(n, int) or n < 0:
        raise ValueError("n muss eine nicht negative ganze Zahl sein.")
    if not tables:
        display(HTML("<p>Keine Tabellen vorhanden.</p>"))
        return
    height, width = max(100, int(max_height)), max(450, int(card_width))
    background = escape(str(theme.get("success_bg", "#EAF8F7")), quote=True)
    border = escape(str(theme.get("success_border", "#168B8A")), quote=True)
    cards = []
    for name, frame in tables.items():
        # Positionsbasiert: funktioniert auch bei nicht eindeutigen Indizes.
        positions = sorted(set(range(min(n, len(frame)))) |
                           set(range(max(n, len(frame) - n), len(frame)))) if n else []
        preview = frame.iloc[positions]
        body = _table_html(preview)
        # Verschiedene Tabellen haben eigene Styler-IDs; Trennlinie lokal setzen.
        if len(frame) > 2 * n and n:
            import re as _re
            table_id = _re.search(r'<table id="([^"]+)"', body).group(1)
            body = (f'<style>#{table_id} tbody tr:nth-child({n + 1}) td,'
                    f'#{table_id} tbody tr:nth-child({n + 1}) th'
                    '{border-top:3px solid #168B8A;}</style>') + body
        cards.append(
            f'<section style="flex:0 0 {width}px;min-width:0;box-sizing:border-box;'
            'border:1px solid #D5E5EB;border-radius:8px;padding:12px;">'
            f'<div style="background:{background};border-left:4px solid {border};'
            'padding:10px;margin-bottom:10px;">'
            f'<b>{escape(str(name))}</b>: {len(frame):,} Zeilen · {frame.shape[1]} Spalten'
            f'<br>Erste / letzte {n} Zeilen (ohne Ueberschneidungen)</div>'
            f'<div style="max-height:{height}px;overflow:auto;">{body}</div></section>'
        )
    display(HTML('<div style="display:flex;flex-wrap:nowrap;gap:16px;'
                 'align-items:flex-start;overflow-x:auto;width:100%;padding-bottom:12px;">'
                 + ''.join(cards) + '</div>'))


def category_distribution(frame, column):
    """Berechnet Haeufigkeiten einer Spalte inklusive fehlender Werte.

    Args:
        frame: Zu untersuchender DataFrame.
        column: Spaltenname, z.B. "flight_booked".

    Returns:
        DataFrame mit Anzahl und Anteil (%) an ALLEN Zeilen.

    Beispiel:
        result = eda.category_distribution(df_sessions, "flight_booked")
        eda.display_table(result, title="Flugbuchungen")
    """
    counts = frame[column].value_counts(dropna=False)
    return pd.DataFrame({
        "Anzahl": counts,
        "Anteil (%)": counts / len(frame) * 100 if len(frame) else np.nan,
    })


def check_duplicates(frame, subset=None):
    """Prueft doppelte Schluessel oder vollstaendig identische Zeilen.

    Args:
        frame: Zu untersuchender DataFrame.
        subset: Liste von Schluesselspalten oder None fuer alle Spalten.

    Returns:
        (Bericht, DataFrame mit ALLEN Zeilen der Duplikatgruppen).
        Wiederholungen nach erstem Auftreten zaehlt nur die Zusatzzeilen.

    Beispiel:
        report, rows = eda.check_duplicates(df_sessions, ["session_id"])

    Wiederholte user_id in Sessions sind erwartbar. Fehlende Schluessel
    koennen von pandas als Duplikate behandelt werden; separat pruefen.
    """
    repeated = frame.duplicated(subset=subset, keep=False)
    extra = frame.duplicated(subset=subset, keep="first")
    summary = pd.DataFrame([{
        "Zeilen": len(frame),
        "Zeilen in Duplikatgruppen": int(repeated.sum()),
        "Wiederholungen nach erstem Auftreten": int(extra.sum()),
    }])
    return summary, frame.loc[repeated].copy()


def check_value_ranges(frame, rules):
    """Prueft numerische Werte gegen inklusive Unter- und Obergrenzen.

    Args:
        frame: Zu untersuchender DataFrame.
        rules: {Spaltenname: (Minimum, Maximum)} mit numerischen Grenzen.

    Returns:
        (Bericht, {Spaltenname: auffaellige Originalzeilen}). Fehlende Werte
        stehen separat im Bericht und nicht in den auffaelligen Zeilen.
        Nicht numerische Werte und Werte ausserhalb der Grenzen werden
        getrennt gezaehlt. Unendlich liegt ausserhalb endlicher Grenzen.

    Beispiel:
        report, rows = eda.check_value_ranges(
            df_users, {"home_airport_lat": (-90, 90)})
    """
    records, affected = [], {}
    for column, (lower, upper) in rules.items():
        if lower > upper:
            raise ValueError(f"Minimum groesser als Maximum: {column}")
        original = frame[column]
        numeric = pd.to_numeric(original, errors="coerce")
        missing = original.isna()
        invalid = ~missing & numeric.isna()
        outside = numeric.notna() & ~numeric.between(lower, upper)
        bad = invalid | outside
        records.append({
            "Spalte": column,
            "Minimum erlaubt": lower,
            "Maximum erlaubt": upper,
            "Fehlend": int(missing.sum()),
            "Nicht numerisch": int(invalid.sum()),
            "Außerhalb Bereich": int(outside.sum()),
        })
        affected[column] = frame.loc[bad].copy()
    return pd.DataFrame(records), affected


def check_expected_types(frame, expected):
    """Vergleicht Zellinhalte mit explizit erwarteten Inhaltstypen.

    Args:
        frame: Zu untersuchender DataFrame.
        expected: {Spaltenname: "Text" | "Zahl" | "Datum" | "Boolean"}.

    Returns:
        (Bericht, {Spaltenname: Originalzeilen mit Typabweichungen}).
        Fehlende Werte werden separat gezaehlt, nicht als Abweichung.

    Beispiel:
        report, rows = eda.check_expected_types(
            df_sessions, {"session_start": "Datum", "page_clicks": "Zahl"})

    Prueft Inhalte, nicht pandas-Speichertypen. Auch "42" gilt als Zahl.
    Numerische IDs deshalb als Zahl erwarten. Fuer Datumsstrings wird
    ISO-Format erwartet. Ein passender Typ garantiert keinen plausiblen Wert.
    """
    records, affected = [], {}
    allowed = {"Text", "Zahl", "Datum", "Boolean"}
    for column, expected_type in expected.items():
        if expected_type not in allowed:
            raise ValueError(f"Unbekannter Inhaltstyp: {expected_type}")
        detected = frame[column].map(detect_value_type)
        mismatch = detected.notna() & detected.ne(expected_type)
        records.append({
            "Spalte": column,
            "Erwarteter Inhaltstyp": expected_type,
            "Fehlend": int(frame[column].isna().sum()),
            "Abweichungen": int(mismatch.sum()),
            "Status": "⚠ Typabweichungen" if mismatch.any() else "✓ Keine Typabweichungen",
        })
        affected[column] = frame.loc[mismatch].copy()
    return pd.DataFrame(records), affected
