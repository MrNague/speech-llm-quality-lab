"""Append auditable listening passes; generate manifest from latest reviews."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import uuid
import wave

from quality_lab.runner.io import atomic_json


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',required=True)
    parser.add_argument('--reviewer',required=True)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    plan=json.loads((root/'data/pilot/recording_plan.json').read_text(encoding='utf-8'))
    entry=next((r for r in plan if r['case_id']==args.case),None)
    if entry is None or not args.reviewer.strip():parser.error('Invalid case or reviewer')
    data=root/'data/local/pilot';audio=data/'audio'/f'{args.case}.wav'
    if not audio.exists():parser.error('Record the audio first')
    print('Listen to the WAV in data/local/pilot/audio using your audio player.')
    if input('Have you listened to the actual audio now? [yes/no] ').strip()!='yes':return
    reference=input('Actual spoken words (keep accents, fillers and omitted ne): ').strip()
    if not reference:parser.error('Empty reference')
    digest=hashlib.sha256(audio.read_bytes()).hexdigest()
    history=data/'reviews.json';events=json.loads(history.read_text(encoding='utf-8')) if history.exists() else []
    previous=[e for e in events if e['case_id']==args.case]
    confirmed=[e for e in previous if e['audio_sha256']==digest and e['reference_text']==reference]
    status='pending'
    if confirmed:
        print('Approval requires a separate listening session at a later time.')
        if input('Is this a second separate listening session, with no ambiguity? [yes/no] ').strip()=='yes':status='approved'
    if input('Is any part unclear? [yes/no] ').strip()=='yes':status='unclear'
    event=dict(review_id=str(uuid.uuid4()),case_id=args.case,reviewer_id=args.reviewer,
               reviewed_at=datetime.now(timezone.utc).isoformat(),audio_sha256=digest,
               reference_text=reference,review_status=status,supersedes=previous[-1]['review_id'] if previous else None)
    events.append(event);atomic_json(history,events)
    # Rebuild only a DEV working manifest. No frozen dataset is modified.
    rows=[]
    for planned in plan:
        reviews=[e for e in events if e['case_id']==planned['case_id']]
        if not reviews:continue
        review=reviews[-1];path=data/'audio'/f"{planned['case_id']}.wav"
        with wave.open(str(path),'rb') as wav:duration=wav.getnframes()/wav.getframerate()
        rows.append(dict(schema_version='1.0',case_id=planned['case_id'],group_id=planned['group_id'],speaker_id='speaker01',
                         audio_path=f"audio/{planned['case_id']}.wav",audio_sha256=review['audio_sha256'],duration_s=duration,sample_rate_hz=16000,
                         reference_text=review['reference_text'],primary_category=planned['primary_category'],tags=['pilot'],split='dev',
                         review_status=review['review_status'],source='Self-recorded fictitious French support request; review history: reviews.json',publication_allowed=False))
    from quality_lab.runner.pilot import atomic_jsonl
    atomic_jsonl(data/'audio_manifest.jsonl',rows)
    print(f"{args.case}: {status}; manifest has {len(rows)} reviewed cases")

if __name__=='__main__':main()
