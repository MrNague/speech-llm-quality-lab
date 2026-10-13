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

@pytest.mark.parametrize('ref',['', '', '  ', '---'])
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

@pytest.mark.parametrize("mode", ["raw", "normalized"])
@pytest.mark.parametrize(
    "reference,prediction,expected",
    [
        ("le chat dort", "le chien dort", (1, 0, 0)),
        ("le chat dort", "le dort", (0, 1, 0)),
        ("le chat dort", "le chat dort ici", (0, 0, 1)),
    ],
)
def test_word_edit_counts(mode, reference, prediction, expected):
    result = corpus_metrics([(reference, prediction)], mode=mode)
    counts = result["words"]

    assert (
        counts["substitutions"],
        counts["deletions"],
        counts["insertions"],
    ) == expected
    assert counts["reference_units"] == 3
    assert result["wer"] == pytest.approx(1 / 3)


@pytest.mark.parametrize("mode", ["raw", "normalized"])
@pytest.mark.parametrize(
    "prediction,expected",
    [
        ("chut", (1, 0, 0)),
        ("cha", (0, 1, 0)),
        ("chats", (0, 0, 1)),
    ],
)
def test_character_edit_counts(mode, prediction, expected):
    result = corpus_metrics([("chat", prediction)], mode=mode)
    counts = result["characters"]

    assert (
        counts["substitutions"],
        counts["deletions"],
        counts["insertions"],
    ) == expected
    assert counts["reference_units"] == 4
    assert result["cer"] == pytest.approx(0.25)


@pytest.mark.parametrize("mode", ["raw", "normalized"])
def test_empty_prediction_word_and_character_rates(mode):
    result = corpus_metrics([("le petit chat dort", "")], mode=mode)

    assert result["wer"] == 1.0
    assert result["cer"] == 1.0
    for unit in ("words", "characters"):
        counts = result[unit]
        assert counts["substitutions"] == 0
        assert counts["insertions"] == 0
        assert counts["deletions"] == counts["reference_units"]


def test_capitalization_raw_and_normalized():
    pairs = [("Bonjour", "bonjour")]

    raw = corpus_metrics(pairs, mode="raw")
    assert raw["wer"] == 1.0
    assert raw["cer"] == pytest.approx(1 / 7)

    normalized = corpus_metrics(pairs, mode="normalized")
    assert normalized["wer"] == 0.0
    assert normalized["cer"] == 0.0


@pytest.mark.parametrize("mode", ["raw", "normalized"])
@pytest.mark.parametrize("reference", [None, "", "   "])
def test_missing_or_empty_reference_rejected(mode, reference):
    with pytest.raises(ValueError):
        corpus_metrics([(reference, "bonjour")], mode=mode)


@pytest.mark.parametrize("mode", ["raw", "normalized"])
def test_missing_reference_message_is_consistent(mode):
    with pytest.raises(ValueError, match="must be a string"):
        corpus_metrics([(None, "bonjour")], mode=mode)
