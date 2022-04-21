from funer.document import Document
from funer.entity_span import EntitySpan
from spacy.lang.en import English


def test_document():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
        gold_label=['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 15, "PER")]
    document.weakly_entities["f2"] = [EntitySpan(28, 32, "LOC")]
    document.weakly_entities["f3"] = [EntitySpan(36, 40, "DATE")]

    assert "Michael Jackson was born in Gary in 1958." == document.text
    assert ['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'] == document.tokens

    span_label = [
        EntitySpan(0, 15, "PER"),    # Michael Jackson
        EntitySpan(28, 32, "LOC"),   # Gary
        EntitySpan(36, 40, "DATE"),  # 1958
    ]
    assert span_label == document.gold_entities
    assert ['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O'] == document.export_bio_label()


def test_document_with_spacy():
    nlp = English()
    tokenizer = nlp.tokenizer

    text = "Michael Jackson was born in Gary in 1958."
    span_label = [
        (0, 15, "PER"),    # Michael Jackson
        (28, 32, "LOC"),   # Gary
        (36, 40, "DATE"),  # 1958
    ]
    document = Document.from_spacy_doc(tokenizer(text), span_label)
    assert text == document.text
    assert ['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'] == document.tokens
    span_label = [
        EntitySpan(0, 15, "PER"),    # Michael Jackson
        EntitySpan(28, 32, "LOC"),   # Gary
        EntitySpan(36, 40, "DATE"),  # 1958
    ]
    assert span_label == document.gold_entities
