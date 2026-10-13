# Shared Storage, API and Diagnostic Specification

Status: draft for M4 (Akepson) and M5 (Michel) — must be agreed before either writes code.
Applies to: M4 items 1, 3, 4, 5, 6 and M5 items 1, 2, 3, 6.
Owner: MrNague. Reviewers: Akepson, Michel.

This file exists so M4 and M5 do not diverge. If either contributor needs to change
something here, open a task issue first and update this file in the same PR.

---

## 1. Runtime data locations

Beta runtime data must live outside the Git repository. "Outside Git" means both
not committed and not written into the working tree.

### 1.1 Roots

| Purpose                 | macOS                                              | Linux / WSL                                        |
|-------------------------|----------------------------------------------------|----------------------------------------------------|
| Runtime root            | `~/Library/Application Support/speech-llm-quality-lab/` | `~/.local/share/speech-llm-quality-lab/`      |
| Config root (optional)  | `~/Library/Application Support/speech-llm-quality-lab/config/` | same pattern                       |
| Cache root              | `~/Library/Caches/speech-llm-quality-lab/`         | `~/.cache/speech-llm-quality-lab/`                 |

Windows-native paths are not used: Michel works in WSL, so the Linux path applies.
A single environment variable `SPEECH_LLM_LAB_HOME` overrides the runtime root in
tests and CI. If unset, the OS default above is used.

### 1.2 Sub-layout of the runtime root

<runtime_root>/
runs/ # one directory per run, id = UUID
diagnostics/ # exported and imported diagnostic packages
outbox/ # packages produced locally, not yet transferred
inbox/ # packages received from a peer
receipts/ # JSON receipt per imported package
annotations/ # critical annotations and review revisions
rubric/ # persisted rubric ratings (illustrative LLM cases included)
tmp/ # atomic-write staging; cleared on startup


### 1.3 Models

Model weights stay where they are now (`models/whisper-tiny/`) or move to
`<runtime_root>/models/`. They are never stored inside `runs/`. User content
(runs, diagnostics, annotations) and model artifacts must be separable by path.

### 1.4 Atomicity

All writes go through the existing `atomic_json` / `atomic_jsonl` helpers in
`src/quality_lab/runner/io.py`. No partial files are left in `runs/`.

### 1.5 Git hygiene

`.gitignore` must exclude the runtime root, diagnostic packages, personal audio,
and any `.wav`/`.mp3`/`.m4a` outside `data/`. Add a test that runs a pilot and
asserts `git status --porcelain` stays empty.

---

## 2. Storage API surface

This is the contract M5 calls. Implemented by M4. File:
`src/quality_lab/storage/__init__.py` (new package).

### 2.1 Result envelope

Every function returns a plain dict:


{
"status": "ok" | "error",
"value": <payload or null>,
"error_code": null | "<short code>",
"message": null | "<human readable>"
}



Failures are never raised as exceptions to the caller and never silently
swallowed. This satisfies M4 item 3 "expose failures honestly".

### 2.2 Functions


save_run(run: dict) -> envelope
Persist a completed or partial run. Rejects if run_id exists.

reopen_run(run_id: str) -> envelope
Return the stored run plus its predictions and metrics.

list_runs(limit: int | None = None) -> envelope
Newest first. Returns summaries only, not full predictions.

delete_run(run_id: str) -> envelope
Deletes the run directory and every derivative. Returns what was removed.

export_diagnostic(run_id: str, fields: list[str], include_audio: bool = False) -> envelope
Builds a package in diagnostics/outbox/. Audio is off unless explicitly
requested. Never transmits anything.

import_diagnostic(package_path: str) -> envelope
Validates, rejects duplicates, writes a receipt, stores under diagnostics/inbox/.

list_imports() -> envelope
Returns receipts: package id, received_at, expires_at, origin label.

delete_import(package_id: str) -> envelope
Deletes the received package and its derivatives. Receipt is marked deleted.

prune(now: datetime | None = None) -> envelope
Applies retention policy. Returns list of removed items and reasons.

preview_fields(run_id: str) -> envelope
Returns the field-by-field preview used by the M5 export dialog.



### 2.3 Error codes (minimum set)

`not_found`, `already_exists`, `invalid_schema`, `path_rejected`, `size_exceeded`,
`duplicate_package`, `expired`, `permission_denied`, `io_error`.

M5 must render every one of these as an explicit UI state (see M5 item 3).

---

## 3. Diagnostic package format

A diagnostic package is a directory. It may be zipped for transfer, but the
canonical form on disk is the directory.

### 3.1 Layout

<package_id>/
manifest.json
fields.json # field-by-field content, per preview_fields()
audio/ # present only if include_audio=True; empty otherwise
README.txt # human-readable: purpose, recipient, retention


### 3.2 manifest.json


{
"package_id": "<uuid>",
"schema_version": "1.0",
"created_at": "<ISO 8601 UTC>",
"app_version": "<from pyproject.toml>",
"origin_label": "<free text, e.g. 'peer review, Michel'>",
"run_id": "<uuid or null>",
"includes_audio": true | false,
"fields": ["wer", "cer", "coverage", "..."],
"expires_at": "<ISO 8601 UTC or null>",
"retention_days": <int or null>
}


### 3.3 Rules

- Audio is **off by default**. Enabling it must be an explicit, previewed action.
- Import validates `schema_version`, `package_id` uniqueness, and every field
  against the same schema used on export.
- Duplicate `package_id` is rejected with `duplicate_package`.
- Import writes a receipt to `diagnostics/receipts/<package_id>.json`.
- Export never sends data. There is no network call anywhere in this module.
  A test must assert no outbound sockets are opened during export or import.

### 3.4 Retention and deletion

- Default retention: 30 days from `received_at` unless the manifest sets
  `retention_days`.
- `prune()` removes expired packages and their derivatives.
- `delete_import()` removes the package, derivatives, and marks the receipt.
- Documentation must state plainly what deletion does **not** cover (backups,
  files already transferred to a third party).

---

## 4. What M5 depends on

Michel may build these M5 pieces now, using the API names above:

- Navigation scaffold and responsive layout (M5 item 1).
- Explicit pending / failed / incomplete / unavailable states (M5 item 3),
  driven by the error codes in section 2.3.
- Six illustrative LLM review cases and rubric persistence layout (M5 items 4–5).

Michel must wait for Akepson to land the storage package before wiring
save / reopen / export / delete / diagnostic controls (M5 item 6).

---

## 5. Open decisions

- [ ] Exact field list for `preview_fields` (needs M3 metrics final list).
- [ ] Whether model weights move into the runtime root or stay in-repo.
- [ ] Default retention period (30 days proposed).
- [ ] Whether `import_diagnostic` accepts a zip as well as a directory.

Resolve each by opening a task issue and updating this file in the same PR.
