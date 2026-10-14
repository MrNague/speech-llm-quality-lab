# M4/M5 Technical Specification — Local Web Beta

Version: 2.0
Date: 2026-10-14
Status: Proposed implementation baseline; peer review required in PR #28.
Owner: Pascal Cabrel Nague. Reviewers: Akepson and Michel.
Tracking: M4 #4 and M5 #5. Neither issue is completed by this document.

## 1. Decision and scope

Replace the Streamlit presentation layer with React, TypeScript and CSS.
Expose existing Python evaluation and storage services through FastAPI.
Preserve existing M3 ASR, metrics and validation logic behind adapters.

This document supersedes the earlier shared-storage draft and the Streamlit
technology choice for M4/M5. Existing PDF requirements remain applicable except
for explicitly amended technology and interface decisions here. This is a
technical addendum, not a claim that the PDFs have been regenerated.

The beta remains single-user, local-first and local-only. Public deployment is
a separate milestone. speechai.naguepc.de is a candidate address, not an existing
deployment. Domain ownership does not provide compute, storage or authentication.

No live LLM generation, RAG, model training, public accounts or automated sharing
is added to beta scope. E2E and Regression pages remain unavailable in this beta.

## 2. Components, languages and boundaries

| Component | Technology | Responsibility |
| --- | --- | --- |
| Browser UI | React, TypeScript, semantic HTML, CSS | Navigation, forms, previews, accessible state rendering |
| Frontend tooling | Vite, Node.js, npm | Development server and production assets |
| HTTP API | Python 3.11, FastAPI, Pydantic | Typed requests, validation, application orchestration |
| Evaluation | Existing Python M3 modules | ASR jobs, WER/CER, coverage and error evidence |
| Storage | Python, versioned JSON/JSONL and managed files | Explicit save, revisions, lifecycle and diagnostic packages |
| Verification | pytest; Vitest/Testing Library; Playwright | Backend, UI components and browser integration |

Use a tested Node release recorded in the repository and a committed
package-lock.json; use npm ci for reproducible installs. Add separately reviewed
API dependency input/lock files. Do not silently upgrade existing ASR locks.
Pin exact framework versions during implementation after compatibility checks.

Planned source layout:
- frontend/src/pages/: eight page components.
- frontend/src/components/: shared navigation, cards, forms and status widgets.
- frontend/src/api/: typed HTTP client; no direct filesystem access.
- frontend/src/styles/: design tokens and responsive CSS.
- src/quality_lab/api/: FastAPI routes and boundary models.
- src/quality_lab/storage/: framework-independent persistence services.
- Existing asr/, evaluation/ and runner/: reusable M3 implementation.
- tests/: backend and contract tests; frontend tests live under frontend/.

The browser calls /api/v1. FastAPI calls Python services; the browser never
imports Python or accesses server paths. Run expensive inference in a bounded
worker process rather than blocking the API request thread.

Development: UI on loopback port 5173, API on loopback port 8000, with a dev proxy
for /api. Packaged beta: FastAPI serves built UI and API from the same loopback
origin. Assets, fonts and icons must work without external CDN requests.

## 3. M5 design contract

Visual references: docs/UI_&_Architecture/. Screen PNGs define visual hierarchy;
architecture.png is a system reference, not a ninth page. Screenshots are design
references, not measured data or proof of implemented functionality.

| Page | Route | Beta content |
| --- | --- | --- |
| Overview | / | Real coverage/status summaries, recent saved runs, next actions |
| Data Quality | /data-quality | Audio import/recording, validation, provenance, reference review |
| ASR Analysis | /asr-analysis | Jobs, predictions, reference comparison, WER/CER, critical annotations |
| LLM Review | /llm-review | Six illustrative cases, fictional sources, editable rubric and revisions |
| E2E Comparison | /e2e-comparison | Explicitly unavailable; outside beta scope |
| Regression | /regression | Explicitly unavailable; outside beta scope |
| Reports | /reports | Saved results, reopen, export and voluntary diagnostic preview |
| Configuration | /configuration | Model/configuration metadata, storage and resource settings |

Use horizontal top navigation, English labels, consistent icons, colors,
typography, spacing and panel hierarchy aligned with the approved images.
Separate ASR reference review from illustrative LLM review. Mockup values must
not become application measurements.

Create explicit CSS tokens for colors, spacing, typography, radii and shadows.
Document visual choices not recoverable precisely from raster images. Require
owner screenshot review rather than claiming pixel-perfect equivalence.

Navigation hover uses a clear background highlight and subtle scale transform
without layout shift; keyboard focus is equally visible. Respect reduced-motion
preferences. At narrow widths use an accessible menu or wrapping layout; no
clipped controls or page-wide horizontal overflow. Wide tables may scroll in
their own labeled region.

Verify layouts at 1440, 768 and 390 CSS pixels. This checks browser responsiveness,
not a smartphone installation package or network access from another device.
UI text is rendered as text; do not inject reference/transcript content as HTML.

## 4. API and state contract

OpenAPI is the typed HTTP contract. Commit an exported schema and generated
TypeScript types; review breaking changes jointly before frontend integration.
Use /api/v1 and UUID identifiers. Reject unknown request fields. Never accept
arbitrary local filesystem paths from browser payloads.

Planned endpoints (contract to implement, not existing APIs):
| Method/path | Purpose |
| --- | --- |
| GET /capabilities | Available operations, model readiness and configured limits |
| POST /drafts | Multipart audio upload; temporary validated draft, not durable save |
| GET /drafts/{id} | Draft validation state and editable reference |
| PATCH /drafts/{id}/reference | Optional reference and its review/provenance metadata |
| POST /jobs | Enqueue a draft snapshot with model/configuration identifiers |
| GET /jobs/{id} | Poll status, progress and terminal result |
| POST /jobs/{id}/cancel | Request worker cancellation; report final state after termination |
| POST /runs | Explicitly save a draft/job snapshot; reject duplicate run ID |
| GET /runs | Paginated summaries |
| GET /runs/{id} | Reopen saved predictions, metrics and revision history |
| POST /runs/{id}/reviews | Append reference/critical-review revision with expected revision |
| DELETE /runs/{id} | Delete owned managed artifacts or report partial failure |
| GET /llm-cases | Six clearly illustrative source/response cases |
| POST /llm-cases/{id}/reviews | Persist rubric revision with expected revision |
| POST /runs/{id}/exports | Export a selected report; does not transmit it |
| POST /runs/{id}/diagnostic-preview | Preview exact selected fields and optional audio |
| POST /runs/{id}/diagnostics | Export the confirmed unchanged preview |
| POST /diagnostics/imports | Upload and validate a diagnostic ZIP |
| GET /diagnostics/imports | List received cases and receipt/expiry metadata |
| DELETE /diagnostics/imports/{id} | Delete received case and managed derivatives |

All paths above are relative to /api/v1. Downloads use opaque managed artifact
IDs, never client-supplied paths. Sensitive downloads require the local session.

Successful JSON responses: {status: "ok", value: payload}.
Errors: {status: "error", value: null, error_code: code, message: safeMessage,
request_id: uuid}. Use meaningful HTTP codes: 400 invalid input, 401 missing
session, 403 denied, 404 absent, 409 duplicate/revision conflict, 413 excessive
size, 422 schema failure, 429 full queue, 503 unavailable capability, 500 internal
failure. Error responses contain no stack trace or local path.

Expected service failures use the existing result-envelope concept.
Unexpected exceptions are caught at the API boundary, logged without content,
and returned as safe internal errors; never turn programming bugs into success.

Keep separate:
- Job state: pending, running, completed, failed, cancelled, timed_out.
- Review state: pending, incomplete, complete.
- Metric state: available, unavailable; value is a fraction or null, plus reason.
- Capability state: available or unavailable, with explanation.

Missing reference: transcription may succeed; metrics are null with
reason missing_reference and UI label "Not available". Empty successful prediction
against a nonempty valid reference is scored as deletions. Failed/cancelled/
timed-out jobs never become empty successful predictions. An empty normalized
reference yields unavailable metrics with an explicit reason. Preserve raw and
normalized results and normalization_version. UI percentages are formatting only.

Edits append revisions. Predictions retain the reference/configuration snapshot
used for evaluation; a changed reference requires explicit re-evaluation and must
not silently rewrite previous evidence. Optimistic revision checks prevent stale
browser updates overwriting a newer review.

## 5. M4 storage and lifecycle

Team environments: Pascal Windows/WSL, Michel Ubuntu, Akepson macOS Apple Silicon.
Support is established through recorded installation and execution evidence, not
assumed from the operating system or chip name.

| Platform | Runtime root | Model cache |
| --- | --- | --- |
| Windows native | %LOCALAPPDATA%/SpeechLLMQualityLab/workspace | %LOCALAPPDATA%/SpeechLLMQualityLab/models |
| Linux/WSL | ${XDG_DATA_HOME:-~/.local/share}/speech-llm-quality-lab | ${XDG_CACHE_HOME:-~/.cache}/speech-llm-quality-lab/models |
| macOS | ~/Library/Application Support/speech-llm-quality-lab | ~/Library/Caches/speech-llm-quality-lab/models |

SPEECH_LLM_LAB_HOME overrides runtime root in tests/development. Reject roots
inside the repository. Models remain separate from user content. Existing
repository-local pilot data/model directories are legacy development inputs;
migration must copy, verify and explicitly confirm before deleting originals.

Runtime directories: runs/, annotations/, rubric/, diagnostics/outbox/,
diagnostics/inbox/, diagnostics/receipts/, tmp/. No user content in Git,
frontend assets, localStorage or browser caches. Static illustrative cases may
remain in Git when clearly labeled and free of personal information.

Uploads and unsaved work are temporary. Explicit Save creates durable data.
Drafts expire after one hour of inactivity; running jobs pin their input.
Reconcile interrupted jobs and clean only validated orphan temporary directories
at startup; never blindly clear every temporary file. Local saved runs remain
until explicit deletion; show this policy before saving. Received diagnostics
expire no later than 30 days after receipt. Outbox packages expire after 24 hours;
report downloads after one hour. Cleanup runs at startup and periodically while
running; expiry is enforced before reads even if physical cleanup is delayed.

Reuse atomic_json/atomic_jsonl only after verifying their failure behavior.
Stage complete multi-file runs and atomically publish them; maintain a derivative
index and serialize writes. An atomic JSON write alone does not make a multi-file
save transactional. Keep original content intact on failed saves.

delete_run and delete_import remove owned audio copies, transcripts, metrics,
reviews and generated managed exports. Shared model cache is not a derivative.
Report partial deletion; retry safely. Minimal tombstones contain IDs/timestamps
only, never original text. Deletion cannot remove externally downloaded copies,
third-party transfers or backups; disclose those limits.

## 6. Local API security and resource limits

Bind both servers to loopback, never 0.0.0.0. No public tunnel or LAN exposure.
Allow only configured Host/Origin values; production uses same-origin requests.
Development CORS, if needed, uses exact origins, never a wildcard. CORS is not
authentication.

A launcher creates an unpredictable per-launch bootstrap secret and exchanges it
once for an HttpOnly SameSite=Strict local session cookie, then clears the secret
from the URL. Do not log or persist it. Require a session for data endpoints and
CSRF protection plus Origin checks for mutations. Local mode does not isolate
data from other processes running as the same OS user. Verify cross-origin and
DNS-rebinding rejection. Content responses use no-store and restrictive CSP.
No telemetry or automatic network uploads; model downloads are explicit setup.

Proposed beta ceilings, to verify on the supported device before acceptance:
| Resource | Limit |
| --- | --- |
| Concurrent ASR workers | 1 |
| Waiting jobs | 2 |
| Audio file | 20 MiB, 60 seconds decoded duration |
| JSON request | 1 MiB |
| Model startup / inference deadline | 180 s / 120 s per case |
| Cancellation | Worker terminates within 5 s of accepted cancellation |
| Total managed workspace | 1 GiB; refuse writes exceeding budget |
| Diagnostic ZIP | 25 MiB compressed, 50 MiB expanded, 100 entries |

Browser recording uses negotiated supported codecs; server decodes supported
WAV/MP3/M4A/WebM/Ogg inputs and validates actual content, duration, channel/sample
limits before inference. Reject unsupported/corrupt input clearly. Do not rely
on extension, MIME or client-side limits. Bound decode time/memory in a worker.
Enforce upload limits during streaming, before buffering/extraction.

On restart, unfinished jobs become interrupted/failed; no automatic expensive
retries. A cancelled or timed-out worker must be reaped before another starts.
Limits are server-enforced and advertised through /capabilities.

## 7. Diagnostic contract

Export is voluntary and local. Recipient: Pascal; purpose: diagnosis and product
improvement. It does not grant permission for training, public release or onward
sharing. Display purpose, recipient and retention before confirmation.

Canonical package: manifest.json, fields.json, README.txt and optional audio/.
The transport is ZIP; browser imports accept uploaded ZIP bytes, not server paths.
Audio defaults off. Preview allows selection, redaction and omission per field.
Export must match the confirmed preview revision or return 409.

Allowlisted optional fields: case identifiers, user-selected reference/prediction,
review notes, critical annotations, raw/normalized WER/CER and edit counts,
coverage, timings, safe error codes, model/configuration/normalization versions
and selected environment versions. Exclude usernames, absolute paths, credentials,
unrelated cases and logs by default. Revalidate every exported field.

Manifest schema 1.0: package_id UUID, created_at UTC, app_version, origin_label
(optional bounded text), run_id optional UUID, includes_audio boolean, selected
field names, member sizes/hashes and requested retention/expiry (optional).
Hashes detect accidental corruption; they do not authenticate the sender.

Strictly validate schema, allowed members, sizes, hashes and content before
publishing an import. Reject unknown versions, duplicates, symlinks, absolute
paths, traversal, nested archives and decompression bombs. No network requests.
Imported identifiers cannot overwrite local runs. Receipt records received_at
and locally computed expires_at: at most received_at + 30 days, shortened by a
valid earlier request. Sender metadata can never extend local retention.
Private manual transfer is separate from export. No public issue attachments.

## 8. Acceptance and migration

| ID | Required evidence |
| --- | --- |
| M4-A | OS paths/override tests; no runtime writes in repository; model separation |
| M4-B | Save/reopen/revisions/crash recovery; stale edit rejection; explicit-save test |
| M4-C | Deletion/partial failure/retry, derivative cleanup, expiry with simulated clock |
| M4-D | Exact redacted preview/export parity; audio off; no outbound traffic |
| M4-E | Malicious ZIP/schema/path/size/duplicate rejection; retention cannot be extended |
| M4-F | Loopback/session/CSRF/Host/Origin tests and bounded job/decode/storage checks |
| M5-A | Eight routes, horizontal navigation and approved screenshot comparison |
| M5-B | Keyboard/focus/contrast/reduced-motion checks at 1440/768/390 px |
| M5-C | Real import-to-result workflow, failed/empty/missing-reference distinctions |
| M5-D | Six illustrative cases, sources, rubric persistence and revision history |
| M5-E | Save/reopen/export/delete/share controls wired to verified M4 behavior |
| M5-F | No mock metrics in normal application; API unavailability shown honestly |

Implement in this order:
1. Review this contract and page mapping jointly.
2. Build React shell and approved layouts; unavailable controls stay disabled.
3. Implement typed FastAPI facade and M4 services; contract-test responses.
4. Integrate M3 jobs/metrics and M4 persistence; run browser lifecycle tests.
5. Remove Streamlit launch instructions/dependencies only when replacement works.
6. Reconcile README, PDFs and issue checklists; link evidence before beta acceptance.

Mock responses are permitted only in automated tests or explicitly labeled visual
fixtures, never as operational results. The merged Streamlit scaffold remains
historical work; fix its loader defect if it remains runnable during transition.
Do not claim an unavailable placeholder verifies missing-reference integration.

Akepson coordinates M4; Pascal and assistant implement the UI migration with Michel
reviewing the design. All three rotate review/testing/explanation roles. Record
actual contributions; AI-generated code does not establish individual mastery.

## 9. Separate public-deployment milestone

Before exposing a service at speechai.naguepc.de, specify hosting/compute cost,
TLS, authenticated users, per-user authorization and isolation, rate/abuse limits,
storage location, consent/retention policy, backup deletion limits, monitoring,
secrets handling and incident recovery. Validate data separation and upload
security with hosted integration tests. A subdomain is configured only after this
review; the local single-user workspace is not a multi-user production backend.

## 10. References

- Existing requirements: M4 issue #4 and M5 issue #5.
- Existing UI baseline: ../UI_&_Architecture/.
- React documentation: https://react.dev/learn
- FastAPI origins: https://fastapi.tiangolo.com/tutorial/cors/
- FastAPI uploads: https://fastapi.tiangolo.com/tutorial/request-files/

These references support framework usage; security and resource ceilings above
are project requirements awaiting implementation and verification.
