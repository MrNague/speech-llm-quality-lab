"""Explicit model download. Never uploads recordings or accepts remote inference."""
import json
from pathlib import Path
from huggingface_hub import HfApi,snapshot_download
from quality_lab.runner.io import atomic_json

root=Path(__file__).resolve().parents[1]
repo='Systran/faster-whisper-tiny'
info=HfApi().model_info(repo)
license_id = info.card_data.get('license') if info.card_data else None
if license_id != 'mit':raise RuntimeError('Model license metadata must be reviewed before download')
revision=info.sha
if not revision:raise RuntimeError('Could not resolve immutable revision')
path=root/'models/whisper-tiny'
if path.exists():raise SystemExit('Model directory exists; keep it for reproducibility. No overwrite performed.')
snapshot_download(repo_id=repo,revision=revision,local_dir=path)
# Local snapshot identity is recorded independently from the eventual benchmark.
atomic_json(path/'quality_lab_model.json',dict(model_id=repo,model_revision=revision,license=license_id,
    source='https://huggingface.co/Systran/faster-whisper-tiny',purpose='AP2 candidate; hardware validation pending'))
print('Model downloaded and revision recorded. Candidate is not yet validated on reference CPU.')
