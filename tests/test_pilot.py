import json
import multiprocessing as mp
from pathlib import Path
from types import SimpleNamespace
import sys
import time
import pytest
from quality_lab.asr.faster_whisper_adapter import FasterWhisperAdapter
from quality_lab.runner.pilot import atomic_jsonl,receive,stop,report_pilot


def test_adapter_local_and_lazy(monkeypatch,tmp_path):
    calls={}
    class FakeModel:
        def __init__(self,path,**kwargs):calls['load']=kwargs
        def transcribe(self,path,**kwargs):
            calls['decode']=kwargs
            def segments():
                calls['consumed']=True
                yield SimpleNamespace(text=' Bonjour')
                yield SimpleNamespace(text=' Pascal.')
            return segments(),None
    monkeypatch.setitem(sys.modules,'faster_whisper',SimpleNamespace(WhisperModel=FakeModel))
    adapter=FasterWhisperAdapter({'model_path':str(tmp_path)})
    result=adapter.transcribe(tmp_path/'x.wav',{})
    assert result['text']=='Bonjour Pascal.' and calls['consumed']
    assert calls['load']['local_files_only'] is True
    assert calls['load']['device']=='cpu'
    assert calls['decode']['language']=='fr'
    assert 'initial_prompt' not in calls['decode']


def sleeping_worker(conn):
    time.sleep(30)


def test_timeout_terminates_process():
    ctx=mp.get_context('spawn');parent,child=ctx.Pipe();proc=ctx.Process(target=sleeping_worker,args=(child,));proc.start();child.close()
    try:
        assert receive(parent,proc,.05)['status']=='timeout'
    finally:stop(proc,parent)
    assert not proc.is_alive()


def test_report_coverage_and_escaping(tmp_path):
    rows=[{'case_id':'a','reference_text':'un deux','primary_category':'negation','duration_s':4},
          {'case_id':'b','reference_text':'trois','primary_category':'negation','duration_s':4}]
    preds=[{'case_id':'a','status':'success','raw_output':'<script>','elapsed_s':2,'rss_bytes':100},
           {'case_id':'b','status':'timeout','raw_output':None,'elapsed_s':120}]
    atomic_jsonl(tmp_path/'inputs.jsonl',rows);atomic_jsonl(tmp_path/'predictions.jsonl',preds)
    report_pilot(tmp_path)
    metrics=(tmp_path/'metrics.json').read_bytes()
    assert json.loads(metrics)['coverage']==.5
    assert json.loads(metrics)['rtf']==.5
    assert '<script>' not in (tmp_path/'report.html').read_text()
    report_pilot(tmp_path)
    assert (tmp_path/'metrics.json').read_bytes()==metrics


def test_plan_balanced_dev_only():
    from collections import Counter
    rows=json.loads((Path(__file__).parents[1]/'data/pilot/recording_plan.json').read_text(encoding='utf-8'))
    assert len(rows)==30 and len({r['case_id'] for r in rows})==30
    assert set(Counter(r['primary_category'] for r in rows).values())=={5}
    assert all(r['split']=='dev' for r in rows)


def fake_worker(conn,config):
    conn.send({'status':'ready','load_s':.01})
    while True:
        try:path=conn.recv()
        except EOFError:break
        if path is None:break
        conn.send({'status':'success','text':'un deux trois','elapsed_s':.1,'rss_bytes':100})


def test_run_persists_valid_contracts(tmp_path,monkeypatch):
    import importlib.util
    from jsonschema import Draft202012Validator
    from quality_lab.runner import pilot
    script=Path(__file__).parents[1]/'scripts/make_fixtures.py'
    spec=importlib.util.spec_from_file_location('create_fixture',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=tmp_path/'data';rows=module.create(data)
    for r in rows:r['review_status']='approved'
    atomic_jsonl(data/'audio_manifest.jsonl',rows)
    model=tmp_path/'model';model.mkdir()
    (model/'quality_lab_model.json').write_text(json.dumps({'model_id':'test-only','model_revision':'fixture'}))
    config=tmp_path/'pilot.json'
    config.write_text(json.dumps({'data_root':'data','manifest':'audio_manifest.jsonl','model_path':'model','runs_root':'runs',
                                 'model_id':'test-only','external_enabled':False,'timeout_s':2,'load_timeout_s':30}))
    monkeypatch.setattr(pilot,'worker',fake_worker)
    monkeypatch.setattr(pilot.importlib.metadata,'version',lambda _: 'fixture')
    assert pilot.run_pilot(config,2)==0
    run_dir=next((tmp_path/'runs').iterdir())
    run=json.loads((run_dir/'run.json').read_text())
    assert run['status']=='completed' and run['planned']==2
    schemas=Path(__file__).parents[1]/'src/quality_lab/data/schemas'
    Draft202012Validator(json.loads((schemas/'run.schema.json').read_text())).validate(run)
    for line in (run_dir/'predictions.jsonl').read_text().splitlines():
        Draft202012Validator(json.loads((schemas/'predictions.schema.json').read_text())).validate(json.loads(line))
    # Independent invocation always allocates a new run and preserves the earlier one.
    original=(run_dir/'run.json').read_bytes()
    assert pilot.run_pilot(config,1)==0
    assert len(list((tmp_path/'runs').iterdir()))==2
    assert (run_dir/'run.json').read_bytes()==original
