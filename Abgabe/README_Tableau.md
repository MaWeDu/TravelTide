# TravelTide – Tableau

## Öffnen
`Abgabe/TravelTide_Tableau.twbx` direkt in Tableau öffnen. Die Datei enthält die Arbeitsmappe, beide Hyper-Extrakte und die zugehörigen CSV-Snapshots. Keine Datenbankanmeldung und keine Pfadanpassung erforderlich. Getestet mit der lokal installierten Tableau Public 2026.2-Anwendung; Tableau Desktop 2026.1 verlangte eine Lizenzaktivierung und wurde nicht zum Prüfen verwendet.

## Inhalt
1. Überblick: Nutzer, Sessions, robuste Empfehlungen, allgemeine Einladung, Segmentgrößen und Entscheidungsstatus.
2. Kundensegmente: Reisen, Hotelnächte, Flugvorlauf und beobachtete Stornoquote.
3. Vorteile und Evidenz: robuste Perk-Hypothesen und noch offene Entscheidungen.
4. Kundenstruktur: Geschlecht, Altersgruppen und Familienstand gemeinsam mit Kindern.
5. Sessions im Zeitverlauf: wöchentlich aktive/buchende Nutzer und Buchungskombinationen.

Die 23 Diagrammblätter sind nativ bearbeitbar. Die gemeinsame Auswahl **Segment auswählen** oben rechts filtert alle fünf Dashboards. Zum Zurücksetzen **Alle** wählen. Einzelwerte lassen sich per Mauszeiger über den Markierungen ablesen. Bei kleinen Bildschirmen Tableau maximieren oder den Präsentationsmodus verwenden.

## Daten und Kennzahlen
- Originalkohorte: 5.998 Nutzer; Stichtag 16.07.2023 (UTC).
- 48.587 eindeutige Sessions; 171 robuste Vorteilshypothesen und 5.827 allgemeine bzw. weitere Prüfaktionen.
- Robuste Empfehlungen: 128 erste Hotelnacht, 38 Gepäck, 5 exklusive Rabatte. Keine robuste automatische Zuordnung zu Mahlzeiten/Stornierung.
- Users enthält genau eine Zeile je Nutzer. Sessions enthält genau eine Zeile je Session; das Segment wurde mit geprüfter n:1-Zuordnung ergänzt. Die Tabellen werden nicht über einen vervielfachenden Session-Join kombiniert.
- Nutzerwerte mit Ø sind ungewichtete Mittelwerte vorhandener Nutzerkennzahlen. Sie können deshalb von den Medianen im Abschlussbericht abweichen.
- Wöchentliche Nutzer sind innerhalb jeder Woche eindeutig gezählt. Ein Nutzer darf in mehreren Wochen vorkommen; Wochenwerte dürfen nicht zu einer Gesamtzahl eindeutiger Nutzer addiert werden.
- Buchungsquote Sessions: Sessions mit `flight_booked` oder `hotel_booked` geteilt durch alle Sessions der Auswahl. Die bestehende Analyse verwendet bekannte Boolean-Werte.
- Stornos sind beobachtete Stornierungs-Sessions zu gebuchten Reisen, kein verifizierter endgültiger Transaktionsstatus.
- Fehlende Daten bleiben fehlend. Perk-Hypothesen sind weder gemessene Präferenzen noch belegte Wirkungen.
- Die erste Sessionwoche kann wegen des Kohortenbeginns unvollständig sein; Daten nach dem Stichtag werden nicht gezeigt.

## Design und Aktualisierung
Die Farben wurden beim Erstellen aus `config.py` übernommen; Tableau liest die Python-Datei beim Öffnen nicht erneut. Die Arbeitsmappe zeigt einen festen, geprüften Snapshot. Neue Daten erfordern eine erneute Erstellung/Aktualisierung der Extrakte und der zugrunde liegenden Features. Cluster und Perks werden in Tableau nicht neu trainiert.

Die ursprünglichen CSV-Dateien und Notebooks wurden nicht verändert. Es wurde nichts zu Tableau Public, Tableau Cloud oder einem Server hochgeladen.
