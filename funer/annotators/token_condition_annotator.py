import copy
from typing import Callable, Iterable, List, Tuple

from funer.annotators.base_annotator import BaseAnnotator
from funer.document import Document


def generate_token_conditions_function(conditions: List[Callable[[str], bool]]):
    n_gram = len(conditions)

    def token_conditions_function(tokens: List[str]) -> Iterable[Tuple[int, int]]:
        for last_i in range(n_gram - 1, len(tokens)):
            if sum([conditions[f_idx](tokens[token_i + last_i - (n_gram - 1)]) for f_idx, token_i in enumerate(range(n_gram))]) == n_gram:
                yield last_i - n_gram + 1, last_i + 1
    return token_conditions_function


class TokensConditionAnnotator(BaseAnnotator):
    def __init__(self,
                 name: str,
                 f: Callable[[List[str]], Iterable[Tuple[int, int]]],
                 label: str) -> None:
        super().__init__(name, label)
        self.f = f

    def match(self,
              document: Document) -> Document:
        new_document = copy.deepcopy(document)
        for start_token_i, end_token_i, in self.f(new_document.tokens):
            new_document.add_token_span_entity(start_token_i, end_token_i, self.label, self.name)
        return new_document
