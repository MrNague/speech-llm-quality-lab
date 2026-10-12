# M3 — Local ASR Validation Evidence

Date: 2026-10-12
Operator: Pascal Cabrel Nague (MrNague), Michel Ange Nji Le (Michel) and Loic Kepguie (Akepson)
Status: Partial validation — M3 acceptance pending

## Environment

- Operating environment: Ubuntu 26.04.1 LTS under WSL on Windows.
- Python: 3.11.17.
- Development dependencies: requirements-dev.lock.
- ASR dependencies: requirements-asr.lock.
- Dependency check: no broken requirements found.
- Automated tests: 46 passed in 9.01 seconds.
- Code commit: 491ed4da32a9e67764e4b9b758dd1691875c9ab4.

## Model provenance

- Model: Systran/faster-whisper-tiny.
- Source: https://huggingface.co/Systran/faster-whisper-tiny
- Revision: d90ca5fe260221311c53c58e660288d3deb8d356.
- License recorded in local model metadata: MIT.
- Local model directory: models/whisper-tiny.
- Model loading succeeded.

## Configuration

| Setting | Value |
| --- | --- |
| Device | CPU |
| Compute type | INT8 |
| CPU threads | 4 |
| Local files only | true |
| Language | French (`fr`) |
| Beam size | 1 |
| Temperature | 0 |
| Condition on previous text | false |

## Input and review status

- Recording: data/lesmis/lesmis_0001.wav.
- Audio duration reported by the decoder: 7.63 seconds.
- Coverage: one unique recording, processed twice.
- Independent reference-review evidence: pending.
- These runs are execution checks, not an accepted corpus benchmark.


## M3 item 1 — Configuration and provenance verification

- Local ASR configuration and model revision are documented above.
- Installed dependencies match requirements-asr.lock for Linux.
- setuptools 75.8.0 and wheel 0.45.1 were explicitly verified.
- Windows-only dependencies are correctly excluded on Linux.
- The full installed dependency snapshot is recorded in
  [M3-wsl-dependencies.txt](M3-wsl-dependencies.txt).
- Model loading and real transcription succeeded using CPU/INT8.

Status: Evidence complete; awaiting peer review.
This status applies only to item 1, not full M3 acceptance.


## Measured results

| Measurement | Run 1 | Run 2 |
| --- | ---: | ---: |
| Model loading | 1.49 s | 1.53 s |
| Transcription time | 3.32 s | 2.50 s |
| Real-time factor | 0.43 | 0.33 |
| Outcome | Completed | Completed |

Real-time factor = transcription time / audio duration.

Model loading was measured separately. Transcription timing included
consuming all generated segments. Both measurements were taken using
Python's perf_counter.

Each run loaded the model in a new Python process. Filesystem cache
conditions were not controlled.

No technical failures were observed in these two executions.

## Model output

Both runs returned the same prediction:

> Chapétre 1. La charébe du faux boure, c'est un d'artouane et la silla du faux boure du temple.

## Interpretation and limitations

- Local ASR execution works in this WSL environment.
- Both executions processed this recording faster than its duration.
- Successful execution does not imply accurate transcription.
- The prediction contains transcription errors requiring evaluation
  against an independently reviewed reference.
- Two runs on one recording do not establish general performance,
  reproducibility across platforms, or corpus-level accuracy.
- Earlier Windows WER/CER results must not be reused for this output:
  the Windows prediction differed.
- Job management, queue limits, timeouts and cancellation were not
  exercised by this direct inference command.
- Results were manually transcribed from terminal output.
- Full hardware validation and M3 acceptance remain pending.
