import copy
from typing import List

from ahocorasick import Automaton
from funer.annotators.base_annotator import BaseAnnotator
from funer.document import Document


class DictionaryAnnotator(BaseAnnotator):
    def __init__(self,
                 name: str,
                 words: List[str],
                 label: str) -> None:
        super().__init__(name, label)
        self.automaton = Automaton()

        for word in words:
            self.automaton.add_word(word, (len(word)))
        self.automaton.make_automaton()

    def match(self,
              document: Document) -> Document:
        new_document = copy.deepcopy(document)
        for end_offset, (entity_length) in self.automaton.iter(new_document.text):
            end_offset += 1
            start_offset = end_offset - entity_length
            new_document.add_char_span_entity(start_offset, end_offset, self.label, self.name)
        return new_document
