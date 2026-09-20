"""Isolated local ASR pilot. Full hash-guarded resume/cache follows in AP3."""
from datetime import datetime,timezone
import hashlib
import html
import importlib.metadata
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import subprocess
import tempfile
from time import perf_counter
import uuid

from quality_lab.data.validation import validate_manifest,safe_path
from quality_lab.evaluation.asr_metrics import corpus_metrics,NORMALIZATION_VERSION
from .io import atomic_json


def atomic_jsonl(path,rows):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);name=None
    try:
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=path.parent,delete=False) as f:
            name=f.name
            for row in rows:f.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n')
            f.flush();os.fsync(f.fileno())
        os.replace(name,path)
    finally:
        if name and os.path.exists(name):os.unlink(name)


def worker(connection,config):
    try:
        import psutil
        from quality_lab.asr.faster_whisper_adapter import FasterWhisperAdapter
        adapter=FasterWhisperAdapter(config)
        connection.send(dict(status='ready',load_s=adapter.load_s))
        while True:
            path=connection.recv()
            if path is None:break
            try:
                result=adapter.transcribe(path,config)
                result.update(status='success',rss_bytes=psutil.Process().memory_info().rss)
                connection.send(result)
            except Exception:
                connection.send(dict(status='inference_error',text=None,elapsed_s=0,error_code='adapter_error'))
    except Exception:
        try:connection.send(dict(status='inference_error',error_code='model_load_error'))
        except (BrokenPipeError,EOFError,OSError):pass
    finally:connection.close()


def receive(connection,process,timeout):
    if not connection.poll(timeout):return dict(status='timeout',error_code='timeout')
    try:return connection.recv()
    except (EOFError,OSError):return dict(status='inference_error',error_code='worker_exit')


def stop(process,connection):
    if process.is_alive():process.terminate()
    process.join(5)
    if process.is_alive():process.kill();process.join()
    connection.close()


def run_pilot(config_path,limit=None):
    config_path=Path(config_path).resolve();config=json.loads(config_path.read_text(encoding='utf-8'));base=config_path.parent
    if config.get('external_enabled') is not False:raise ValueError('Pilot requires external_enabled=false')
    root=(base/config['data_root']).resolve()
    result=validate_manifest(root,config['manifest'])
    if not result['valid']:raise ValueError('Manifest invalid; run validate first')
    rows=[json.loads(s) for s in (root/config['manifest']).read_text(encoding='utf-8').splitlines()]
    for row in rows:
        corpus_metrics([(row['reference_text'], '')])  # Reject punctuation-only references before inference.
    if any(r['split']!='dev' or r['review_status']!='approved' for r in rows):
        raise ValueError('Every pilot manifest case must be approved and DEV')
    if limit is not None:
        if limit<1:raise ValueError('Limit must be positive')
        rows=rows[:limit]
    model=(base/config['model_path']).resolve()
    identity=json.loads((model/'quality_lab_model.json').read_text(encoding='utf-8'))
    if identity['model_id']!=config['model_id'] or not identity.get('model_revision'):raise ValueError('Model identity mismatch')
    timeout=float(config['timeout_s']);load_timeout=float(config['load_timeout_s'])
    if not 0<timeout<=3600 or not 0<load_timeout<=3600:raise ValueError('Invalid timeout')
    run_id=str(uuid.uuid4());out=(base/config['runs_root']).resolve()/run_id;out.mkdir(parents=True,exist_ok=False)
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=base,text=True).strip()
    except (OSError,subprocess.CalledProcessError):commit='unknown'
    model_hash=hashlib.sha256()
    for path in sorted(p for p in model.rglob('*') if p.is_file() and '.cache' not in p.parts):
        model_hash.update(path.relative_to(model).as_posix().encode())
        with path.open('rb') as f:
            for block in iter(lambda:f.read(1024*1024),b''):model_hash.update(block)
    versions={name:importlib.metadata.version(name) for name in ['faster-whisper','ctranslate2','av','psutil']}
    run=dict(schema_version='1.0',run_id=run_id,status='running',started_at=datetime.now(timezone.utc).isoformat(),finished_at=None,
             code_commit=commit,dataset_hash=hashlib.sha256((root/config['manifest']).read_bytes()).hexdigest(),kb_hash='not-applicable-asr',
             config_hash=hashlib.sha256(config_path.read_bytes()).hexdigest(),model_id=identity['model_id'],model_revision=identity['model_revision'],
             prompt_hash='not-applicable-asr',normalization_version=NORMALIZATION_VERSION,environment=dict(python=platform.python_version(),os=platform.system(),packages=versions),cost_status='local-no-provider-cost',
             model_files_hash=model_hash.hexdigest(),planned=len(rows),scope='DEV pilot; not final benchmark',config=config,model_load_s=None)
    atomic_json(out/'run.json',run);atomic_jsonl(out/'inputs.jsonl',rows)
    context=mp.get_context('spawn');parent,child=context.Pipe();process=context.Process(target=worker,args=(child,{**config,'model_path':str(model)}));process.start();child.close()
    predictions=[];failures=0;ready=False
    try:
        loaded=receive(parent,process,load_timeout);ready=loaded.get('status')=='ready';run['model_load_s']=loaded.get('load_s')
        for row in rows:
            start=perf_counter()
            if not ready or failures>=3:
                response=dict(status='skipped',text=None,error_code='worker_unavailable',elapsed_s=0)
            else:
                try:parent.send(str(safe_path(root,row['audio_path'])))
                except (BrokenPipeError,EOFError,OSError):ready=False
                response=receive(parent,process,timeout) if ready else dict(status='inference_error',error_code='worker_exit')
                failures=0 if response['status']=='success' else failures+1
                if response['status']=='timeout':stop(process,parent);ready=False
            prediction=dict(schema_version='1.0',run_id=run_id,case_id=row['case_id'],branch='asr',status=response['status'],raw_output=response.get('text'),
                            parsed_output={'text':response['text']} if response.get('text') is not None else None,elapsed_s=response.get('elapsed_s',perf_counter()-start),
                            error_code=response.get('error_code'),retrieved_passage_ids=[],rss_bytes=response.get('rss_bytes'))
            predictions.append(prediction);atomic_jsonl(out/'predictions.jsonl',predictions)
        run['status']='completed' if all(p['status']=='success' for p in predictions) else ('partial' if ready or any(p['status']=='success' for p in predictions) else 'failed')
        run['load_error']=None if loaded.get('status')=='ready' else loaded.get('error_code')
    except BaseException:
        run['status']='failed';raise
    finally:
        stop(process,parent);run['finished_at']=datetime.now(timezone.utc).isoformat();atomic_json(out/'run.json',run)
    report_pilot(out)
    print(f"Run {run_id}: {run['status']}; report: runs/{run_id}/report.html")
    return 0 if run['status']=='completed' else 2


def report_pilot(out):
    out=Path(out)
    rows=[json.loads(s) for s in (out/'inputs.jsonl').read_text(encoding='utf-8').splitlines()]
    preds=[json.loads(s) for s in (out/'predictions.jsonl').read_text(encoding='utf-8').splitlines()]
    lookup={p['case_id']:p for p in preds};successful=[r for r in rows if lookup[r['case_id']]['status']=='success']
    pairs=[(r['reference_text'],lookup[r['case_id']]['raw_output']) for r in successful]
    duration=sum(r['duration_s'] for r in successful)
    metrics=dict(planned=len(rows),successful=len(successful),coverage=len(successful)/len(rows) if rows else None,
                 raw=corpus_metrics(pairs,'raw'),normalized=corpus_metrics(pairs),
                 rtf=sum(lookup[r['case_id']]['elapsed_s'] for r in successful)/duration if duration else None,
                 rss_sample_max_bytes=max((p.get('rss_bytes') or 0 for p in preds),default=0),categories={})
    for category in sorted({r['primary_category'] for r in rows}):
        subset=[r for r in successful if r['primary_category']==category]
        metrics['categories'][category]=dict(planned=sum(r['primary_category']==category for r in rows),successful=len(subset),small_sample=len(subset)<5,
             metrics=corpus_metrics([(r['reference_text'],lookup[r['case_id']]['raw_output']) for r in subset]))
    atomic_json(out/'metrics.json',metrics)
    table=''.join('<tr>'+''.join('<td>'+html.escape(str(value))+'</td>' for value in [r['case_id'],lookup[r['case_id']]['status'],r['reference_text'],lookup[r['case_id']]['raw_output']])+'</tr>' for r in rows)
    report='<!doctype html><meta charset="utf-8"><title>ASR DEV pilot</title><h1>ASR DEV pilot</h1><p>Single speaker, fictitious support domain. No final benchmark or generalization claim. RSS is sampled after cases, not peak RAM. Slots and resumability are not implemented yet.</p><pre>'+html.escape(json.dumps(metrics,ensure_ascii=False,indent=2))+'</pre><table><tr><th>Case</th><th>Status</th><th>Reference</th><th>Hypothesis</th></tr>'+table+'</table>'
    (out/'report.html').write_text(report,encoding='utf-8')
