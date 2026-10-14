# Diagnostics Specifications

## Recipient and Purpose
Diagnostic packages are strictly intended for the project's developers. Their sole purpose is to allow offline debugging of a failed "run" without exposing the user's entire environment.

## Private Transfer Procedure
These packages must **never** be published on the internet or versioned on GitHub. Transfer to a developer must occur exclusively via a private communication channel (secure direct message).

## Retention and Deletion Limits
- **Retention**: Packages imported onto a developer's machine have a strict lifespan and automatically expire after 7 days.
- **Limits**: If a user deletes a run locally, the action is irreversible. However, this deletion cannot technically destroy a diagnostic package that has already been exported and sent to a third party.