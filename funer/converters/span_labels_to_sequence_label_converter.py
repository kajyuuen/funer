from typing import List

from funer.converters.utils import create_charid_to_tokenid
from funer.entity_span import EntitySpan


class SpanLabelsToSequenceLabelConverter:
    @staticmethod
    def entity_spans2bio(tokens: List[str],
                         spaces: List[bool],
                         entity_spans: List[EntitySpan],
                         no_entity: str = "O") -> List[str]:
        aligned_labels = [no_entity] * len(tokens)
        for span_annotation in entity_spans:
            # Store the token indexes of the annotation
            annotation_token_index_set = set()
            charid_to_tokenid = create_charid_to_tokenid(tokens, spaces)
            for ner_char_index in range(span_annotation.start_offset, span_annotation.end_offset):
                token_index = charid_to_tokenid[ner_char_index]
                if token_index is None:
                    continue
                annotation_token_index_set.add(token_index)

            # 1 token <-> 1 ne
            if len(annotation_token_index_set) == 1:
                token_index = annotation_token_index_set.pop()
                aligned_labels[token_index] = f"B-{span_annotation.label}"
                continue

            # N tokens <-> 1 ne
            for token_cnt, token_index in enumerate(sorted(annotation_token_index_set)):
                if token_cnt == 0:
                    prefix = "B"
                else:
                    prefix = "I"
                aligned_labels[token_index] = f"{prefix}-{span_annotation.label}"
        return aligned_labels
