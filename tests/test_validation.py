import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest
from quality_lab.data.validation import safe_path, validate_manifest

spec=importlib.util.spec_from_file_location('fixtures',Path(__file__).parents[1]/'scripts/make_fixtures.py')
fixtures=importlib.util.module_from_spec(spec); spec.loader.exec_module(fixtures)

@pytest.fixture
def dataset(tmp_path):
    return tmp_path,fixtures.create(tmp_path)

def save(root,rows):
    (root/'audio_manifest.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')

def test_ten_valid_fixtures(dataset):
    root,rows=dataset
    result=validate_manifest(root)
    assert result==dict(valid=True,total=10,approved=0,errors=[])

def test_T01_collects_all_errors(dataset):
    root,rows=dataset
    rows[0]['audio_path']='missing.wav'
    rows[1]['case_id']=rows[2]['case_id']
    rows[3]['duration_s']='three'
    rows[4]['audio_path']='../outside.wav'
    save(root,rows)
    result=validate_manifest(root)
    assert not result['valid']
    codes={e['code'] for e in result['errors']}
    assert {'missing_audio','duplicate_id','schema_error','unsafe_path'} <= codes
    assert all(e['case_id'] for e in result['errors'])

@pytest.mark.parametrize('path',['/etc/passwd','../escape.wav','a/../../escape.wav','C:/secret.wav','C:secret.wav','\\\\host\\share','a\\..\\secret'])
def test_unsafe_paths(tmp_path,path):
    with pytest.raises(ValueError):safe_path(tmp_path,path)

def test_external_symlink(dataset,tmp_path):
    root,rows=dataset
    target=root.parent/'external.wav';target.write_bytes(b'outside')
    link=root/'link.wav'
    try:link.symlink_to(target)
    except OSError:pytest.skip('Symlink creation requires privilege on this OS')
    rows[0]['audio_path']='link.wav';save(root,rows)
    assert 'unsafe_path' in {e['code'] for e in validate_manifest(root)['errors']}

@pytest.mark.parametrize('change,code',[
    ({'audio_sha256':'0'*64},'hash_mismatch'),
    ({'duration_s':4},'duration_mismatch'),
    ({'reference_text':'   '},'empty_reference'),
    ({'publication_allowed':'false'},'schema_error'),
    ({'duration_s':True},'schema_error'),
    ({'schema_version':'2.0'},'schema_error'),
])
def test_invalid_record(dataset,change,code):
    root,rows=dataset;rows[0].update(change);save(root,rows)
    assert code in {e['code'] for e in validate_manifest(root)['errors']}

@pytest.mark.parametrize('key,code',[('group_id','group_split_leakage'),('audio_sha256','hash_split_leakage'),('reference_text','text_split_leakage')])
def test_split_leakage(dataset,key,code):
    root,rows=dataset;rows[1][key]=rows[0][key];rows[1]['split']='test';save(root,rows)
    assert code in {e['code'] for e in validate_manifest(root)['errors']}

@pytest.mark.parametrize('raw',['','\n','{','[]','{"duration_s":NaN}'])
def test_bad_jsonl(tmp_path,raw):
    (tmp_path/'audio_manifest.jsonl').write_text(raw)
    assert not validate_manifest(tmp_path)['valid']

def test_corrupt_wave(dataset):
    root,rows=dataset;(root/rows[0]['audio_path']).write_bytes(b'broken')
    assert 'invalid_wav' in {e['code'] for e in validate_manifest(root)['errors']}

def test_cli_success_failure_and_report(dataset):
    root,rows=dataset
    config=root/'config.json';output=root/'validation.json'
    config.write_text(json.dumps(dict(schema_version='1.0',data_root='.',manifest='audio_manifest.jsonl',output='validation.json')))
    command=[sys.executable,'-m','quality_lab','validate','--config',str(config)]
    assert subprocess.run(command,capture_output=True).returncode==0
    assert json.loads(output.read_text())['valid']
    rows[0]['audio_path']='missing.wav';save(root,rows)
    assert subprocess.run(command,capture_output=True).returncode==2
    assert not json.loads(output.read_text())['valid']
    assert not list(root.glob('tmp*'))

def test_all_schemas_are_valid():
    from jsonschema import Draft202012Validator
    for path in (Path(__file__).parents[1]/'src/quality_lab/data/schemas').glob('*.json'):
        Draft202012Validator.check_schema(json.loads(path.read_text()))

@pytest.mark.parametrize('config_text',['[]','null','{}','{'])
def test_cli_bad_config(tmp_path,config_text):
    config=tmp_path/'bad.json';config.write_text(config_text)
    result=subprocess.run([sys.executable,'-m','quality_lab','validate','--config',str(config)],capture_output=True,text=True)
    assert result.returncode==2
    assert json.loads(result.stdout)['errors'][0]['code']=='configuration_or_io_error'
