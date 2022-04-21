from funer.annotators.dictionary_annotator import DictionaryAnnotator
from funer.document import Document


def test_dictionary_annotator():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
        gold_label=['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']
    )

    dictionary_annotator = DictionaryAnnotator(
        name="f1",
        words=["Michael Jackson"],
        label="NAME"
    )
    new_document = dictionary_annotator.match(document)
    assert "Michael Jackson" == \
        new_document.text[new_document.weakly_entities["f1"][0].start_offset:new_document.weakly_entities["f1"][0].end_offset]
