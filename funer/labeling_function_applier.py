from dataclasses import dataclass
from typing import Any, List

import texttable

from funer.annotators.base_annotator import BaseAnnotator
from funer.document import Document


@dataclass
class MatchResult:
    num_positive: int = 0
    num_negative: int = 0


class LabelingFunctionApplier:
    def __init__(self, lfs: List[BaseAnnotator]) -> None:
        self.lfs = lfs
        self.match_results = None

    def apply(self, documents: List[Document]) -> List[Document]:
        new_documents = []
        for document in documents:
            for lf in self.lfs:
                document = lf.match(document)

            if document.gold_entities is not None:
                if self.match_results is None:
                    self.match_results = {lf.name: MatchResult() for lf in self.lfs}
                for l_name, weakly_entities in document.weakly_entities.items():
                    for weakly_entity in weakly_entities:
                        is_same = False
                        for gold_entity in document.gold_entities:
                            if weakly_entity.start_offset == gold_entity.start_offset \
                                and weakly_entity.end_offset == gold_entity.end_offset \
                                    and weakly_entity.label == gold_entity.label:
                                is_same = True
                                break
                        if is_same:
                            self.match_results[l_name].num_positive += 1
                        else:
                            self.match_results[l_name].num_negative += 1

            new_documents.append(document)
        return new_documents

    def show_stats(self):
        if self.match_results is None:
            raise ValueError("The apply function has not yet been executed.")
        table = texttable.Texttable()
        table.set_deco(texttable.Texttable.HEADER |
                       texttable.Texttable.VLINES)
        table.set_max_width(0)
        table.set_header_align(["l", "c", "c", "c"])
        table.set_cols_dtype(["t", "i", "i", "i"])

        rows: List[List[Any]] = [["f_name", "pos", "neg", "hit"]]

        for f_name, match_result in self.match_results.items():
            rows.append([f_name, match_result.num_positive, match_result.num_negative, match_result.num_positive + match_result.num_negative])
        table.add_rows(rows)
        return table.draw()
