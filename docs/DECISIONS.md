# Entscheidungen

## E01 – Referenzgerät bestätigt

Pascal bestätigt: Windows 11 Pro, Intel Celeron N5100, 4 Kerne / 4 logische Prozessoren, 32 GB RAM, Intel UHD Graphics mit gemeinsam genutztem RAM, SATA SSD 1 TB mit ca. 600 GB frei. Quelle: Benutzerangaben und Task-Manager-Screenshot im Projektgespräch.

Installation auf dem Referenzgerät: Python 3.11.9, requirements-dev.lock und editable Paket erfolgreich installiert. Vom Benutzer übermitteltes pytest-Protokoll: 30 passed, 1 skipped in 17.53s. Der Symlink-Test wurde wegen fehlender Berechtigung übersprungen; er bestand zuvor unter Linux. Diese Windows-Testlücke bleibt dokumentiert. Hardwareinventar wurde lokal erzeugt, seine JSON-Datei wurde noch nicht übermittelt. Keine Inferenzleistung gemessen; E02 bleibt offen.

## E02 – Modelle: offen

Zwei mehrsprachige Whisper-Konfigurationen und ein französischfähiges lokales Instruct-Modell werden nach Pilot und Lizenzprüfung gewählt. Keine Gewichte heruntergeladen; keine Kompatibilität behauptet.

## E03 – Externe Inferenz

Deaktiviert; Budget 0 EUR. AP1 enthält keinen externen Inferenzpfad.

## E04 – Veröffentlichungsumfang

Persönliche Aufnahmen bleiben lokal. Veröffentlichung ist eine separate spätere Handlung.

## E05 – Reviewer

Selbstbewertung als Standard; Einschränkung offenlegen. Externer Reviewer optional.

## Technische Ausgestaltung AP1

JSON Schema Draft 2020-12, schema_version 1.0. Relative POSIX-Pfade auch unter Windows; Backslashes werden als nicht portabel abgelehnt. Kernreferenzen müssen nicht leer sein. Metadaten-Dauer muss innerhalb eines Samples zur WAV-Dauer passen. Diese Ausgestaltung verändert keine MUSS-Anforderung. Zusätzliche Metadaten erfordern eine dokumentierte Schemaweiterentwicklung.

## E02 – AP2 Pilotkandidat

Systran/faster-whisper-tiny (mehrsprachig), faster-whisper 1.2.1, CPU int8, vier Threads, beam_size 1. Der Download löst die Modellrevision auf und speichert den unveränderlichen Commit. Kandidat, keine endgültige Auswahl: reale N5100-Inferenz und Lizenznachweis des heruntergeladenen Standes sind vor Benchmarkfreigabe zu prüfen. Die Downloadquelle nennt MIT. Quellen: https://huggingface.co/Systran/faster-whisper-tiny und https://github.com/SYSTRAN/faster-whisper . Keine Leistungsbehauptung.
