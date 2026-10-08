# Les Misérables Validation Dataset

## Purpose

This dataset provides a small French speech evaluation corpus for development and validation of the ASR pipeline.

## Source

- Source: Les Misérables (public domain text)
- Language: French
- Format: WAV audio files

## Contents

- 20 audio-reference pairs
- Metadata stored in:
  - `data/labels/lesmis_validation.csv`
  - `data/labels/lesmis_validation.xlsx`
- Audio files stored in:
  - `data/audio/lesmis/`

## Metadata schema

| Column | Description |
|----------|----------|
| audio_path | Relative path to the audio file |
| reference_text | Original reference transcript |
| validated_text | Reviewed transcript |
| duration_sec | Audio duration in seconds |
| review_status | Review state |

## Validation

- CSV encoding verified (UTF-8)
- Audio paths verified
- Audio files existence verified
- Independent review: pending
