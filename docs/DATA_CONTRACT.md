# Datenvertrag AP1

Verbindliche Quelle: Pflichtenheft Kapitel 2 und 3. Implementierte Schemata: `src/quality_lab/data/schemas/`.

Audio-Hauptkategorien: `numbers_times`, `homophones`, `elisions_boundaries`, `negation`, `technical_ids`, `colloquial_variants` entsprechen den sechs Kategorien der Spezifikation in dieser Reihenfolge.

Die zehn Fixtures sind synthetische Softwaredaten mit `review_status=pending` und `publication_allowed=false`. Die Referenztexte beschreiben Testfälle und transkribieren keine tatsächliche Sprache. Niemals als Modellinput/Benchmark oder Teil der 120 freigegebenen Aufnahmen verwenden.

T01 prüft Typen, Pflichtfelder, fehlende Audiodateien, doppelte IDs, SHA-256, WAV PCM16 mono 16 kHz, Dauer 3–20 s, leere Referenzen und Pfade einschließlich externer Symlinks. Erste Gruppen-, Hash- und Textprüfungen entdecken splitübergreifende Duplikate. Die Textprüfung vereinheitlicht derzeit NFC, Kleinschreibung und Leerraum; vollständige normalisierte Duplikatkontrolle und manuelle Vorlagenprüfung folgen in AP3. T02 ist damit noch nicht erfüllt.

Weitere Dateischemata sind strukturelle Grundlagen. Offene fachliche Prüfungen: Slotäquivalenzen, Goldbelege und Begründungen bei fehlenden Goldbelegen, Verknüpfungen der LLM-/Audiofälle, Mengen/Verteilungen, UTC- und Run-Invarianten, Rubrikrevisionen, Provenienz- und Freeze-Nachweise. Sie müssen vor Nutzung der entsprechenden Pipeline umgesetzt sein.
