import pytest
from quality_lab.evaluation.asr_metrics import normalize,corpus_metrics

@pytest.mark.parametrize('hyp',['un deux cinq quatre','un deux quatre','un deux trois quatre cinq'])
def test_T04_one_edit(hyp):
    assert corpus_metrics([('un deux trois quatre',hyp)])['wer']==.25

def test_T04_weighted_corpus():
    r=corpus_metrics([('un','deux'),('un deux trois quatre cinq six sept huit neuf','un deux trois quatre cinq six sept huit neuf')])
    assert r['wer']==.1
    assert r['words']['reference_units']==10

def test_empty_hypothesis_and_insertions():
    assert corpus_metrics([('un deux','')])['wer']==1
    assert corpus_metrics([('un','un deux trois')])['wer']==2
    assert corpus_metrics([])['wer'] is None

@pytest.mark.parametrize('ref',['','   ','---'])
def test_empty_reference_rejected(ref):
    with pytest.raises(ValueError):corpus_metrics([(ref,'bonjour')])

def test_T05_normalization():
    assert normalize("  L’été, dix-huit : je n’ai PAS accès ! ")== 'l été dix huit je n ai pas accès'
    assert normalize('e\u0301')=='é'
    assert normalize('8') != normalize('18')
    assert normalize('ne marche pas') != normalize('marche')
    assert normalize('  A  B! ','raw')=='A  B!'

def test_cer_denominators():
    assert corpus_metrics([('chat','chut')])['cer']==.25
    assert corpus_metrics([('a b','ab')],'raw')['cer']==1/3
    assert corpus_metrics([('a b','ab')])['cer']==0
    assert corpus_metrics([('été','été')])['wer']==0
