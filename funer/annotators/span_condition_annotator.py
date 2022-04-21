import copy
from typing import Callable, Iterable, Tuple

from funer.annotators.base_annotator import BaseAnnotator
from funer.document import Document


class SpanConditionAnnotator(BaseAnnotator):
    def __init__(self,
                 name: str,
                 f: Callable[[str], Iterable[Tuple[int, int]]],
                 label: str) -> None:
        super().__init__(name, label)
        self.f = f

    def match(self,
              document: Document) -> Document:
        new_document = copy.deepcopy(document)
        for start_offset, end_offset, in self.f(new_document.text):
            new_document.add_char_span_entity(start_offset, end_offset, self.label, self.name)
        return new_document
