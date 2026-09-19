"""AP1 input validation; never imports or invokes an inference adapter."""
import hashlib
import json
import math
from pathlib import Path, PureWindowsPath
import unicodedata
import wave
from importlib.resources import files

from jsonschema import Draft202012Validator


def safe_path(root, value):
    root = Path(root).resolve()
    if not isinstance(value, str) or not value or '\\' in value:
        raise ValueError('Expected a relative POSIX path')
    candidate = Path(value)
    if candidate.is_absolute() or PureWindowsPath(value).drive or '..' in candidate.parts:
        raise ValueError('Absolute paths and traversal are forbidden')
    resolved = (root / candidate).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError('Path escapes data root')
    return resolved


def validate_manifest(root, manifest='audio_manifest.jsonl'):
    errors, rows = [], []
    def fail(line, case_id, code, field):
        errors.append(dict(line=line, case_id=case_id, code=code, field=field))
    schema = json.loads(files('quality_lab.data').joinpath('schemas/audio_manifest.schema.json').read_text())
    validator = Draft202012Validator(schema)
    try:
        raw = safe_path(root, manifest).read_text(encoding='utf-8')
    except (OSError, ValueError, UnicodeError):
        fail(0, None, 'manifest_unreadable', 'manifest')
        return dict(valid=False, total=0, approved=0, errors=errors)
    seen, groups, hashes, texts = set(), {}, {}, {}
    for line, text in enumerate(raw.splitlines(), 1):
        try:
            row = json.loads(text, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except (ValueError, TypeError):
            fail(line, None, 'invalid_json', 'record'); continue
        case_id = row.get('case_id') if isinstance(row, dict) else None
        problems = sorted(validator.iter_errors(row), key=lambda e: str(list(e.path)))
        if problems:
            for problem in problems:
                fail(line, case_id, 'schema_error', '.'.join(map(str, problem.path)) or 'record')
            continue
        rows.append(row)
        if case_id in seen: fail(line, case_id, 'duplicate_id', 'case_id')
        seen.add(case_id)
        if not row['reference_text'].strip(): fail(line, case_id, 'empty_reference', 'reference_text')
        if not math.isfinite(row['duration_s']): fail(line, case_id, 'invalid_duration', 'duration_s')
        norm = ' '.join(unicodedata.normalize('NFC', row['reference_text']).casefold().split())
        for mapping, key, code in [(groups,row['group_id'],'group_split_leakage'),(hashes,row['audio_sha256'],'hash_split_leakage'),(texts,norm,'text_split_leakage')]:
            if key in mapping and mapping[key] != row['split']: fail(line, case_id, code, 'split')
            mapping[key] = row['split']
        try:
            audio = safe_path(root, row['audio_path'])
        except (ValueError, OSError):
            fail(line, case_id, 'unsafe_path', 'audio_path'); continue
        try:
            content = audio.read_bytes()
        except OSError:
            fail(line, case_id, 'missing_audio', 'audio_path'); continue
        if hashlib.sha256(content).hexdigest() != row['audio_sha256']:
            fail(line, case_id, 'hash_mismatch', 'audio_sha256')
        try:
            with wave.open(str(audio), 'rb') as stream:
                n, width, rate, frames, compression, _ = stream.getparams()
                data = stream.readframes(frames)
                if (n,width,rate,compression) != (1,2,16000,'NONE'):
                    fail(line, case_id, 'invalid_audio_format', 'audio_path')
                if len(data) != frames*n*width:
                    fail(line, case_id, 'truncated_audio', 'audio_path')
                duration = frames/rate
                if not 3 <= duration <= 20 or abs(duration-row['duration_s']) > 1/rate:
                    fail(line, case_id, 'duration_mismatch', 'duration_s')
        except (wave.Error, EOFError, OSError, ZeroDivisionError):
            fail(line, case_id, 'invalid_wav', 'audio_path')
    if not raw.strip(): fail(0, None, 'empty_manifest', 'manifest')
    return dict(valid=not errors, total=len(rows), approved=sum(r['review_status']=='approved' for r in rows), errors=errors)
