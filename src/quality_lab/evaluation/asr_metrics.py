"""Versioned corpus metrics. Rates are fractions; insertions can make WER > 1."""
import unicodedata
NORMALIZATION_VERSION = "fr-v1"


def normalize(text, mode="normalized"):
    if mode not in {"raw", "normalized"}:
        raise ValueError("Unknown text mode")
    text = unicodedata.normalize("NFC", text).strip()
    if mode == "raw":
        return text
    text = text.lower()
    text = "".join(" " if c in "'’ʼ＇" or unicodedata.category(c) == "Pd" else c
                   for c in text)
    text = "".join(c for c in text if not unicodedata.category(c).startswith("P"))
    return " ".join(text.split())


def edits(reference, hypothesis):
    # Deterministic tie order: match/substitution, deletion, insertion.
    previous = [(j, 0, 0, j) for j in range(len(hypothesis)+1)]
    for i, r in enumerate(reference, 1):
        current = [(i, 0, i, 0)]
        for j, h in enumerate(hypothesis, 1):
            cost, s, d, ins = previous[j-1]
            sub = (cost+(r != h), s+(r != h), d, ins)
            cost, s, d, ins = previous[j]
            delete = (cost+1, s, d+1, ins)
            cost, s, d, ins = current[j-1]
            insert = (cost+1, s, d, ins+1)
            current.append(min((sub, delete, insert), key=lambda x: x[0]))
        previous = current
    _, s, d, i = previous[-1]
    return {"substitutions": s, "deletions": d, "insertions": i,
            "errors": s+d+i, "reference_units": len(reference)}


def corpus_metrics(pairs, mode="normalized"):
    words = dict(substitutions=0, deletions=0, insertions=0, errors=0, reference_units=0)
    chars = words.copy()
    count = 0
    for reference, hypothesis in pairs:
        ref, hyp = normalize(reference, mode), normalize(hypothesis, mode)
        if not ref:
            raise ValueError("Empty reference after normalization")
        w = edits(ref.split(), hyp.split())
        c = edits(ref if mode == "raw" else ref.replace(" ", ""),
                  hyp if mode == "raw" else hyp.replace(" ", ""))
        for key in words:
            words[key] += w[key]; chars[key] += c[key]
        count += 1
    return {"normalization_version": NORMALIZATION_VERSION, "mode": mode, "cases": count,
            "wer": words["errors"]/words["reference_units"] if words["reference_units"] else None,
            "cer": chars["errors"]/chars["reference_units"] if chars["reference_units"] else None,
            "words": words, "characters": chars}
