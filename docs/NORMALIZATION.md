# ASR normalization and corpus metrics

## Version

Current normalization version: `fr-v2`.

Both metric results and pilot run metadata record this version.
Historical `fr-v1` reports remain unchanged. Comparisons across versions
require re-evaluation with the same rules.

## Raw mode

- Apply Unicode NFC normalization.
- Remove leading and trailing whitespace.
- Preserve capitalization, punctuation and internal whitespace.
- WER tokenizes using whitespace.
- CER includes internal spaces.

## Normalized mode

Apply the same rules to the reference and prediction:

- Apply Unicode NFC, trim and lowercase.
- Preserve `.`, `,`, `:` and `/` when immediately between decimal digits.
- Preserve ASCII minus before a digit, including intervening whitespace.
- Preserve Unicode minus as a symbol.
- Replace apostrophes and other unpreserved dash punctuation with spaces.
- Remove remaining Unicode punctuation.
- Collapse whitespace.
- WER tokenizes using whitespace.
- CER excludes spaces.

Accents, digits and negation words are retained.

## Scope and limitations

Normalization is a text transformation, not a numerical or semantic parser.

- `1,5` and `15` remain different.
- `1.5` and `15` remain different.
- `-5` and `5` remain different.
- `1,5` and `1.5` are not treated as equivalent.
- Written number words are not converted to digits.
- ASCII and Unicode minus signs are not unified.
- Spaced and unspaced signs may produce different WER tokenization.
- Other numeric formats are not comprehensively supported.
- Punctuation removal can join text; normalized scores must be interpreted
  alongside raw scores and critical-error review.

## Corpus aggregation

Corpus WER = total word edits / total reference words.
Corpus CER = total character edits / total reference characters.

These are pooled rates, not arithmetic averages of per-case rates.
Edits comprise substitutions, deletions and insertions.
Insertions can make a rate exceed 100%.

## Empty inputs

A successful empty prediction against a valid nonempty reference is
scored as deletions.

The metric function rejects references that are empty after normalization.
An empty collection returns unavailable rates (`None`).

Technical failures must not be substituted with successful empty predictions.

## Verification

Date: 2026-10-19
Environment: Pascal's WSL development environment
Command: `python -m pytest -q -rs`
Result: 80 passed in 25.77 seconds.

Regression tests first demonstrated that `fr-v1` erased decimal separators
and ASCII minus signs. The added regression tests pass under `fr-v2`.

This evidence verifies the tested software behavior, not completion of
the real-speech benchmark or all M3 acceptance criteria.
