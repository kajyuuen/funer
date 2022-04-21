

from funer.converters.sequence_label_to_span_labels_converter import (
    SequenceLabelToSpanLabelsConverter, bio2entity_spans_about_token_ids)
from funer.entity_span import EntitySpan


def test_bio2entity_spans_about_token_id():
    bio_label = ["B-LOC", "B-LOC", "I-LOC", "I-LOC", "O", "B-LOC", "B-PER"]
    entity_spans_about_token_ids = bio2entity_spans_about_token_ids(bio_label)

    assert ["B-LOC"] == bio_label[entity_spans_about_token_ids[0][0]:entity_spans_about_token_ids[0][1]]
    assert "LOC" == entity_spans_about_token_ids[0][2]

    assert ["B-LOC", "I-LOC", "I-LOC"] == bio_label[entity_spans_about_token_ids[1][0]:entity_spans_about_token_ids[1][1]]
    assert "LOC" == entity_spans_about_token_ids[1][2]

    assert ["B-LOC"] == bio_label[entity_spans_about_token_ids[2][0]:entity_spans_about_token_ids[2][1]]
    assert "LOC" == entity_spans_about_token_ids[2][2]

    assert ["B-PER"] == bio_label[entity_spans_about_token_ids[3][0]:entity_spans_about_token_ids[3][1]]
    assert "PER" == entity_spans_about_token_ids[3][2]


def test_one_entity_bio2entity_spans_about_token_id():
    bio_label = ["B-LOC", "I-LOC", "I-LOC", "I-LOC"]
    entity_spans_about_token_ids = bio2entity_spans_about_token_ids(bio_label)

    assert ["B-LOC", "I-LOC", "I-LOC", "I-LOC"] == bio_label[entity_spans_about_token_ids[0][0]:entity_spans_about_token_ids[0][1]]
    assert "LOC" == entity_spans_about_token_ids[0][2]


def test_o_only_bio2entity_spans_about_token_id():
    bio_label = ["O", "O", "O"]
    entity_spans_about_token_ids = bio2entity_spans_about_token_ids(bio_label)

    assert 0 == len(entity_spans_about_token_ids)


def test_align_tokens_and_bio_annotations():
    tokens = ['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.']
    spaces = [True, True, True, True, True, True, True, False, False]
    bio_labels = ['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']

    entity_spans = [
        EntitySpan(0, 15, "PER"),   # Michael Jackson
        EntitySpan(28, 32, "LOC"),  # Gary
        EntitySpan(36, 40, "DATE")  # 1958
    ]
    assert entity_spans == SequenceLabelToSpanLabelsConverter.bio2entity_spans(tokens, spaces, bio_labels)
