from typing import List, Optional

from funer.converters.span_labels_to_sequence_label_converter import (
    SpanLabelsToSequenceLabelConverter, create_charid_to_tokenid)
from funer.entity_span import EntitySpan


def rebuild_text(text: str,
                 tokens: List[str],
                 charid_to_tokenid: List[Optional[int]]) -> str:
    rebuilded_text = ""
    prev_token_id = None
    token_char_i = 0
    for i in range(len(text)):
        token_id = charid_to_tokenid[i]

        if prev_token_id == token_id:
            token_char_i += 1
        else:
            token_char_i = 0

        if token_id is not None:
            rebuilded_text += tokens[token_id][token_char_i]
        else:
            rebuilded_text += " "
        prev_token_id = token_id
    return rebuilded_text


def test_create_charid_to_tokenid():
    tokens = ['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.']
    spaces = [True, True, True, True, True, True, True, False, False]
    charid_to_tokenid = create_charid_to_tokenid(tokens, spaces)
    text = "Michael Jackson was born in Gary in 1958."
    assert text == rebuild_text(text, tokens, charid_to_tokenid)


def test_create_charid_to_tokenid_jp():
    tokens = ['あらゆる', '現実', 'を', 'すべて', '自分 ', 'の', 'ほう', 'へ', 'ねじ曲げ', 'た', 'の', 'だ', '。']
    spaces = [False] * len(tokens)
    charid_to_tokenid = create_charid_to_tokenid(tokens, spaces)
    text = "あらゆる現実をすべて自分 のほうへねじ曲げたのだ。"
    assert text == rebuild_text(text, tokens, charid_to_tokenid)


def test_align_tokens_and_bio_annotations():
    tokens = ['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.']
    spaces = [True, True, True, True, True, True, True, False, False]
    entity_spans = [
        EntitySpan(0, 15, "PER"),   # Michael Jackson
        EntitySpan(28, 32, "LOC"),  # Gary
        EntitySpan(36, 40, "DATE")  # 1958
    ]
    assert ['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O'] == \
        SpanLabelsToSequenceLabelConverter.entity_spans2bio(tokens, spaces, entity_spans)
