# Speech & LLM Quality Lab

Lokales Portfolio-Projekt zur französischen Sprachdatenprüfung und späteren ASR-/LLM-Evaluation. Verbindlich sind die unverändert abgelegten PDFs in `docs/specifications/`.

## Stand: AP1

Implementiert: Python-Paket, sieben JSON-Schemata, Audio-Manifestvalidierung, zehn reproduzierbare künstliche Fixtures, CLI, Tests und Hardwarediagnose. Die sechs weiteren Dateischemata definieren zunächst Pflichtfelder und Grundtypen; ihre fachlichen Beziehungen und vollständigen Invarianten werden in AP3–AP5 implementiert. Die Validierung prüft aktuell das Audio-Manifest, nicht den vollständigen 120/60-Fälle-Bestand.

Keine echten Sprachaufnahmen, Modellläufe, Scores oder fertige Oberfläche enthalten. Fixtures enthalten synthetische PCM-Daten ohne Sprache und zählen nicht als geprüfte Aufnahmen. `app.py` meldet diesen Stand ausdrücklich.

## Installation unter Windows (PowerShell)

Zielversion: Python 3.11. Pascal hat die Installation unter Windows 11 Pro / Python 3.11.9 bestätigt: 30 Tests bestanden, Symlink-Test mangels Berechtigung übersprungen. Unter Linux / Python 3.12 bestanden alle 31 Tests.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
.\.venv\Scripts\python.exe scripts/make_fixtures.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m quality_lab validate --config configs/dev.json
.\.venv\Scripts\python.exe scripts/hardware_probe.py --output artifacts/hardware-reference.json
```

Linux/macOS: `python3.11 -m venv .venv`, danach dieselben Befehle mit `.venv/bin/python`.
Installation kann Netz benötigen. Tests, Fixture-Erstellung, Validierung und Hardwareinventar führen keine externen Anfragen aus. Sie benötigen keine Modelle oder Schlüssel.

`validate`: Exit 0 bei gültigem Manifest, sonst 2. Bericht: `artifacts/validation.json`. Mehrere Fehler werden gemeinsam mit Fall-ID, Zeile, Feld und Fehlercode gemeldet; unlesbare Datensätze haben gegebenenfalls keine Fall-ID. Ungültige Eingaben lösen keine Inferenz aus. `run`, `evaluate`, `compare`, `report` folgen in späteren APs und sind noch nicht verfügbar.

## Aufbau

- `src/quality_lab/`: data, asr, retrieval, generation, evaluation, runner, reporting.
- `tests/`: T01, Audiointegrität, sichere Pfade, erste Splitprüfungen und CLI.
- `scripts/`: reproduzierbare Fixtures und E01-Inventar.
- `docs/`: PDFs, Entscheidungslog, Datenvertrag und Nachweise.
- `data/local/`, `runs/`, `models/`: lokale Daten bleiben außerhalb der Versionskontrolle.

Die Bibliothek `jsonschema` vermeidet eine zweite handgeschriebene Implementierung des JSON-Schema-Standards. pytest ist nur eine Entwicklungsabhängigkeit. pandas, scikit-learn, Streamlit und Inferenzbibliotheken werden mit dem jeweiligen Arbeitspaket samt getesteten Versionen ergänzt.

## Nächster Schritt

E01 ist dokumentiert. Nächster Schritt AP2: Annotation Guide, 30 echte Aufnahmen, erster ASR-Adapter und Handtestmetriken. E02 wird nach Hardware-/Lizenzpilot entschieden; ein Fixture ist kein Modellnachweis.

## Herkunft und Veröffentlichung

Eigenständiges Projekt von Pascal Cabrel Nague, kein Auftrag von KENBUN. PDFs bleiben unverändert. Keine öffentliche Freigabe der Stimme oder des Repositories impliziert. Softwarelizenz vor Veröffentlichung entscheiden; Modelle benötigen eigene Lizenzeinträge.
