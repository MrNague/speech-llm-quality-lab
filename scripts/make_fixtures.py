"""Generate ten deterministic synthetic fixtures, not speech or benchmark results."""
import hashlib
import json
from pathlib import Path
import struct
import wave


def create(root):
    root = Path(root); root.mkdir(parents=True,exist_ok=True)
    rows = []
    categories=['numbers_times','homophones','elisions_boundaries','negation','technical_ids','colloquial_variants']
    for i in range(10):
        audio=root/f'fixture_{i:02}.wav'
        with wave.open(str(audio),'wb') as w:
            w.setparams((1,2,16000,0,'NONE','not compressed'))
            w.writeframes(struct.pack('<h',i)*48000)
        rows.append(dict(schema_version='1.0',case_id=f'FIX{i:02}',group_id=f'GROUP{i:02}',speaker_id='synthetic',audio_path=audio.name,audio_sha256=hashlib.sha256(audio.read_bytes()).hexdigest(),duration_s=3,sample_rate_hz=16000,reference_text=f'Ceci est le cas fictif numéro {i}.',primary_category=categories[i%6],tags=['software_fixture'],split='dev',review_status='pending',source='Synthetic PCM fixture; no speech; not a benchmark',publication_allowed=False))
    (root/'audio_manifest.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
    return rows

if __name__=='__main__':
    create(Path(__file__).resolve().parents[1]/'tests/fixtures/generated')
