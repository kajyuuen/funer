import re

from funer.annotators.dictionary_annotator import DictionaryAnnotator
from funer.annotators.token_condition_annotator import (
    TokensConditionAnnotator, generate_token_conditions_function)
from funer.document import Document
from funer.labeling_function_applier import LabelingFunctionApplier


def test_labeling_function_applyer():
    # Define labeling function
    # labeling function 1
    def detect_gary(tokens):
        for i in range(len(tokens) - 1):
            if tokens[i:i + 1] == ["Gary"]:
                yield i, i + 1
    f1 = TokensConditionAnnotator(
        name="correct_f1",
        f=detect_gary,
        label="LOC"
    )

    # labeling function 2
    nomatch_f2 = TokensConditionAnnotator(
        name="nomatch_f2",
        f=generate_token_conditions_function([
            lambda token: re.search(r"20\d{2}年", token) is not None,  # Wrong rule
        ]),
        label="DATE"
    )

    # labeling function 3
    person_dictionary = ["Michael Jackson", "John Winston", "Tom"]
    f3 = DictionaryAnnotator(
        name="correct_f3",
        words=person_dictionary,
        label="PER"
    )

    # labeling function 4
    person_dictionary = ["was"]
    wrong_f4 = DictionaryAnnotator(
        name="wrong_f4",
        words=person_dictionary,
        label="PER"
    )

    # labeling function 5
    person_dictionary = ["1985"]
    correct_f5 = DictionaryAnnotator(
        name="correct_f5",
        words=person_dictionary,
        label="DATE"
    )

    # Document
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
        gold_label=['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']
    )
    document_2 = Document(
        tokens=['This', 'philosophy', 'was', 'published', 'in', '1985', '.'],
        spaces=[True, True, True, True, True, True, False, False],
        gold_label=['O', 'O', 'O', 'O', 'O', 'B-DATE', 'O']
    )

    # Apply
    lf_applier = LabelingFunctionApplier(lfs=[f1, nomatch_f2, f3, wrong_f4, correct_f5])
    [document, _] = lf_applier.apply([document, document_2])

    assert 'Michael Jackson was born in Gary in 1958.' == document.text
    assert 3 == len(document.weakly_entities)

    assert """f_name     | pos | neg | hit
===========+=====+=====+====
correct_f1 | 1   | 0   | 1  
nomatch_f2 | 0   | 0   | 0  
correct_f3 | 1   | 0   | 1  
wrong_f4   | 0   | 2   | 2  
correct_f5 | 1   | 0   | 1  """ == lf_applier.show_stats()
