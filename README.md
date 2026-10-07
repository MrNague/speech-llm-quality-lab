# Speech & LLM Quality Lab

A personal engineering and learning project for evaluating French speech-to-text outputs and reviewing language-model responses.

The goal is to build a usable application that makes errors understandable, evaluation results traceable, and user data manageable.

We are a two-person team. We work together on every component so that both contributors can explain its design, demonstrate its behavior, and discuss its limitations.

**Status:** Under active development. The revised peer beta is not yet released.

## What the project investigates

The project explores three related questions:

1. **Data quality:** Does the reference accurately represent what was said?
2. **Model quality:** What errors does the model produce, and how important are they?
3. **Software quality:** Does the application process, measure, display, store, and share results correctly?

These are different concerns. An incorrect reference can produce a misleading score. A model can make a mistake while the evaluation tool works correctly. An incorrect metric is a defect in the tool itself.

## Current implementation

The repository contains an initial foundation and ASR pilot tooling:

- A Python package and command-line interface.
- JSON schemas and audio-manifest validation.
- Synthetic audio fixtures for software testing.
- Hardware inventory tooling.
- Recording and reference-review scripts.
- An ASR pilot runner and local model preparation tooling.
- Raw and normalized WER/CER calculations.
- Pilot reporting and automated tests.

**Existing tooling does not mean the revised beta has passed acceptance.**

Real recording evidence, reference-device inference results, installation on a second supported computer, and the revised security checks still need to be completed or verified.

`app.py` is currently a placeholder, not a finished dashboard.

Synthetic PCM fixtures contain no real speech. They test software behavior and do not count as approved recordings or evidence of model quality.

Historical AP1 validation on Windows 11 Pro with Python 3.11.9 reported **30 passed tests and one skipped symlink test**. This historical result does not establish acceptance of the revised beta.

## First usable beta

The first release targets local installation on each tester’s own computer.

### Required scope

- Import or record a short French audio sample.
- Validate the input before inference.
- Run one real local ASR configuration.
- Display audio, transcript, and an optional reviewed reference.
- Calculate WER/CER only when a valid reference exists.
- Show coverage, failures, timings, and critical-error annotations.
- Include at least 12 approved real audio–text pairs.
- Review six clearly labeled illustrative LLM response cases.
- Support explicit saving, persistent review revisions, export, and deletion.
- Collect voluntary feedback and selected diagnostic cases.
- Provide an installation guide and release evidence.

### Outside the first beta

- Public web hosting or shared user accounts.
- Cloud inference.
- Live LLM generation.
- Model training or fine-tuning.
- A complete RAG pipeline.
- A fully automated end-to-end benchmark.
- A general claim of robustness across French speakers or accents.
- A smartphone installation package.

The LLM review examples are illustrative. Their ratings must not be presented as measured performance of a real LLM.

## How we work together

Both contributors participate in every part of the project:

1. Understand the problem and requirements.
2. Discuss alternatives and make a design decision.
3. Implement or integrate the solution while reviewing its behavior.
4. Switch roles within the component.
5. Test normal behavior and failure scenarios.
6. Explain and demonstrate the result individually.
7. Record evidence, assistance received, and remaining questions.

We divide activities, not permanent areas of knowledge.

AI assistance may support implementation, testing, and explanations. Generated code is not treated as proof that either contributor has mastered the underlying concepts.

Each contributor maintains their own competency evidence.

**Working language:** English for project discussions, new documentation, and the planned interface. French remains the language of the speech evaluation cases. Some existing implementation messages and historical guides still require translation.

## Schedule

Joint work is planned to start on **7 October 2026**, with approximately eight hours together per day, including breaks.

The provisional peer-beta release target is **13 October 2026**, subject to acceptance evidence. Starting on 7 October leaves six development days before that date.

If seven complete working days are needed, development finishes on 13 October and release moves to 14 October.

The deadline does not override correctness, data protection, or security requirements. An incomplete build will be labeled as a preview rather than an accepted beta.

## Data storage and voluntary sharing

### Current development tooling

Existing pilot tooling uses repository-local working directories such as:

- `data/local/`
- `runs/`
- `models/`

These are local development locations. Do not commit personal recordings, transcripts, model weights, credentials, or diagnostic packages.

### Planned beta storage

The revised architecture moves runtime user data outside the source repository.

Windows:

```text
%LOCALAPPDATA%\SpeechLLMQualityLab\workspace
```

Linux, if support is validated:

```text
${XDG_DATA_HOME:-~/.local/share}/speech-llm-quality-lab/workspace
```

Model weights are stored separately from user content.

This storage migration and its protections are requirements to implement and verify; they are not claimed as completed.

### Sharing a diagnostic case

The planned **Share this case with Pascal** workflow lets a tester:

1. Select one case.
2. Inspect the fields and purpose of sharing.
3. Edit or exclude optional content.
4. Choose whether to include audio, which defaults to off.
5. Confirm export.
6. Manually transfer the package through an agreed private channel.

Export does not automatically send data.

Received cases are stored separately from Git and retained for up to 30 days from receipt under the defined deletion procedure. Sharing for diagnosis does not authorize publication, model training, or onward distribution.

## Security requirements

The beta must demonstrate:

- Local-only access, without a public listener or tunnel.
- No automatic user-data uploads or telemetry.
- Strict file, schema, size, and path validation.
- Safe handling of user text and exported content.
- Bounded inference time, queue length, and storage usage.
- Explicit saving and verifiable deletion of managed data.
- Safe validation of received diagnostic packages.
- Tested installation dependencies and documented model provenance.

Localhost is not authentication. Local files are not automatically encrypted by the application. Backups and copies exported outside managed storage remain outside its deletion guarantees.

These are release requirements, not a security certification.

## Development setup

Run these commands from the repository root.

### Windows PowerShell

Prerequisite: Python 3.11.

```powershell
py -3.11 -m venv .venv

.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .

.\.venv\Scripts\python.exe scripts/make_fixtures.py
.\.venv\Scripts\python.exe -m pytest -q -rs

.\.venv\Scripts\python.exe -m quality_lab validate --config configs/dev.json

.\.venv\Scripts\python.exe scripts/hardware_probe.py --output artifacts/hardware-reference.json
```

These commands verify the development foundation. They do not launch a finished user interface or prove real ASR performance.

Dependency installation may require internet access. Fixture generation and manifest validation do not require model weights or API keys.

### ASR pilot tooling

The existing pilot workflow is documented in:

- [AP2 setup guide](docs/AP2_START.md)
- [Annotation guide](docs/ANNOTATION_GUIDE.md)
- [Pilot recording sheet](docs/PILOT_RECORDING_SHEET.md)

These guides describe the earlier AP2 workflow, including its 30-recording target. They must be reconciled with the revised 12-case beta scope before being used as the new acceptance checklist.

Real inference requires the optional ASR dependencies, prepared local model weights, and valid reviewed recordings.

### Platform support

Windows 11 x64 is the primary beta target.

Linux support requires a separate installation and execution check. macOS, ARM, and smartphone support are not currently promised.

## Technology choices

| Part | Language, format, or tool |
|---|---|
| Application logic, validation, storage, ASR, and metrics | Python |
| Planned interface | Python with Streamlit |
| Interface styling and reports | HTML and CSS |
| Windows setup | PowerShell |
| Optional Linux setup | Bash |
| Structured data and exports | JSON, JSONL, CSV |
| Configuration | TOML |
| Tests | Python and pytest |
| Documentation and version control | Markdown and Git |

JSON, CSV, and TOML are data/configuration formats. Git is a tool, not a programming language.

JavaScript, TypeScript, SQL, Docker, Kubernetes, and CUDA are not requirements for the first beta. Additional technologies require a justified architecture decision.

## Repository structure

```text
src/quality_lab/   Python modules and component interfaces
tests/            Automated software tests
scripts/          Fixtures, hardware inventory, and pilot utilities
configs/          Development and pilot configurations
docs/             Specifications, guides, decisions, and evidence
data/local/       Local development data
runs/             Local pilot results
app.py            Dashboard placeholder
```

Some directories represent planned components rather than completed services.

## Project documentation

The revised planning baseline consists of:

| Document | Version | Purpose |
|---|---|---|
| User Requirements Specification | 2.2 | Needs, scope, constraints, and acceptance criteria |
| Technical Design Specification | 2.2 | Architecture, data lifecycle, security, and verification |
| Competency Portfolio | 1.1 | Demonstrated skills, learning objectives, and career profiles |

The English documents use Times New Roman.

The document set should be maintained under `docs/specifications/`. Older documents and AP guides are historical references where they conflict with the revised baseline.

The latest agreement also establishes two-person collaboration on every component and a 7 October start. These changes must be incorporated into the next specification revision; earlier staffing assumptions and dated schedules are superseded.

Pascal’s existing competency portfolio is personal. The second contributor needs a separate record rather than inheriting Pascal’s experience or achievements.

## Release criteria

Before inviting classmates to use an accepted beta, we need evidence that:

- The real ASR workflow works on the reference computer.
- A fresh installation works on a second supported computer.
- Metrics match independently checked examples.
- Missing results and incomplete reviews remain visible.
- Saving, reopening, exporting, sharing, and deletion behave correctly.
- Required security tests pass.
- Illustrative results cannot be mistaken for real model measurements.
- Instructions, known limitations, and test guidance are available.

A poor model prediction is an evaluation finding. Incorrect metrics, data loss, or unauthorized disclosure are release-blocking defects.

## Project ownership and licensing

This is an independent personal project initiated by Pascal Cabrel Nague and now developed collaboratively by two contributors.

Software licensing must be explicitly settled before public distribution. Model weights, datasets, recordings, and third-party dependencies have separate licensing and permission requirements.

Access to a recording does not automatically grant permission to publish it, redistribute it, or use it for training.
