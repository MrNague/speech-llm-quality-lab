"""Record one local PCM16/16kHz mono case. Never overwrites an existing take."""
import argparse
import hashlib
import json
from pathlib import Path
import wave


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',required=True)
    parser.add_argument('--seconds',type=int,default=12,choices=range(3,21))
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    plan=json.loads((root/'data/pilot/recording_plan.json').read_text(encoding='utf-8'))
    row=next((r for r in plan if r['case_id']==args.case),None)
    if row is None: parser.error('Unknown case ID')
    destination=root/'data/local/pilot/audio'/f'{args.case}.wav'
    if destination.exists(): parser.error('Take exists. Archive it before recording a replacement.')
    import sounddevice as sd
    print(row['script_text'])
    input(f'Press Enter, then speak. Recording duration: {args.seconds}s. ')
    chunks=[]
    with sd.RawInputStream(samplerate=16000,channels=1,dtype='int16') as stream:
        for _ in range(args.seconds*10):
            data,overflow=stream.read(1600)
            if overflow: raise RuntimeError('Input overflow: recording discarded; retry with fewer background apps')
            chunks.append(bytes(data))
    destination.parent.mkdir(parents=True,exist_ok=True)
    with destination.open('xb') as f:
        with wave.open(f,'wb') as wav:
            wav.setparams((1,2,16000,0,'NONE','not compressed'));wav.writeframes(b''.join(chunks))
    print(f'Saved {args.case}. Listen and review twice before approval.')

if __name__=='__main__':main()
