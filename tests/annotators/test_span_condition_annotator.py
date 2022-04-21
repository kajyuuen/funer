import re

from funer.annotators.span_condition_annotator import SpanConditionAnnotator
from funer.document import Document


def test_span_condition_annotator():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
    )

    def span_condition_function(text: str):
        for m in re.finditer(r"Michael Jackson", text):
            yield m.start(), m.end()

    spans_condition_annotator = SpanConditionAnnotator(
        name="f1",
        f=span_condition_function,
        label="NAME"
    )
    new_document = spans_condition_annotator.match(document)
    assert "Michael Jackson" == \
        new_document.text[new_document.weakly_entities["f1"][0].start_offset:new_document.weakly_entities["f1"][0].end_offset]
