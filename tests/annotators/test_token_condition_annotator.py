from typing import List

from funer.annotators.token_condition_annotator import (
    TokensConditionAnnotator, generate_token_conditions_function)
from funer.document import Document


def test_token_condition_annotator():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
        gold_label=['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']
    )

    def token_conditions_function(tokens: List[str]):
        for i in range(len(tokens) - 1):
            if tokens[i:i + 2] == ["Michael", "Jackson"]:
                yield i, i + 2

    tokens_condition_annotator = TokensConditionAnnotator(
        name="f1",
        f=token_conditions_function,
        label="NAME"
    )
    new_document = tokens_condition_annotator.match(document)
    assert "Michael Jackson" == \
        new_document.text[new_document.weakly_entities["f1"][0].start_offset:new_document.weakly_entities["f1"][0].end_offset]


def test_generate_token_conditions_function():
    document = Document(
        tokens=['Michael', 'Jackson'],
        spaces=[True, True],
    )

    tokens_condition_annotator = TokensConditionAnnotator(
        name="f1",
        f=generate_token_conditions_function([
            lambda token_1: token_1 == "Michael",
            lambda token_2: token_2 == "Jackson",
        ]),
        label="NAME"
    )
    new_document = tokens_condition_annotator.match(document)
    assert "Michael Jackson" == \
        new_document.text[new_document.weakly_entities["f1"][0].start_offset:new_document.weakly_entities["f1"][0].end_offset]


def test_no_match_token_condition_annotator():
    document = Document(
        tokens=['Michael', 'Jackson'],
        spaces=[True, True],
    )

    tokens_condition_annotator = TokensConditionAnnotator(
        name="f1",
        f=generate_token_conditions_function([
            lambda token_1: token_1 == "Michael",
            lambda token_2: token_2 == "・",
            lambda token_3: token_3 == "Jackson",
        ]),
        label="NAME"
    )
    new_document = tokens_condition_annotator.match(document)
    assert new_document.weakly_entities["f1"] == []
