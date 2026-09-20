"""Atomic local JSON writes."""
import json
import os
from pathlib import Path
import tempfile


def atomic_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as f:
            temp = f.name
            json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if temp and os.path.exists(temp): os.unlink(temp)
