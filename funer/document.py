from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from spacy.tokens import Doc
from spacy.training.iob_utils import offsets_to_biluo_tags

from funer.converters.sequence_label_to_sequence_label import \
    SequenceLabelToSequenceLabelConverter
from funer.converters.sequence_label_to_span_labels_converter import \
    SequenceLabelToSpanLabelsConverter
from funer.converters.span_labels_to_sequence_label_converter import \
    SpanLabelsToSequenceLabelConverter
from funer.entity_span import EntitySpan


class Document:
    def __init__(self,
                 tokens: List[str],
                 spaces: Optional[List[bool]] = None,
                 gold_label: Optional[List[str]] = None):
        self.tokens = tokens
        self.spaces = spaces if spaces is not None else [False] * len(self.tokens)
        self.text = "".join([token + " " if is_space else token for token, is_space in zip(tokens, self.spaces)])

        self.gold_entities: Optional[List[EntitySpan]] = \
            SequenceLabelToSpanLabelsConverter.bio2entity_spans(self.tokens, self.spaces, gold_label) if gold_label is not None else None
        self.weakly_entities: Dict[str, List[EntitySpan]] = defaultdict(list)
        self.aggregated_entities: Optional[List[EntitySpan]] = None

    @classmethod
    def from_spacy_doc(cls,
                       doc: Doc,
                       gold_entities: Optional[List[Tuple[int, int, str]]] = None):
        tokens, spaces = [], []
        for token in doc:
            tokens.append(token.text)
            spaces.append(token.whitespace_ != "")
        bilou_label = offsets_to_biluo_tags(doc, gold_entities) if gold_entities is not None else None
        label = SequenceLabelToSequenceLabelConverter.bilou2bio(bilou_label) if bilou_label is not None else None
        return cls(tokens, spaces, label)

    def add_token_span_entity(self,
                              start_token_i: int,
                              end_token_i: int,
                              label: str,
                              annotator_name: str):
        start_offset = len("".join(self.tokens[:start_token_i])) + sum(self.spaces[:start_token_i])
        end_offset = start_offset + len("".join(self.tokens[start_token_i:end_token_i])) + sum(self.spaces[start_token_i:end_token_i - 1])
        self.weakly_entities[annotator_name].append(EntitySpan(start_offset, end_offset, label))

    def add_char_span_entity(self,
                             start_offset: int,
                             end_offset: int,
                             label: str,
                             annotator_name: str):
        self.weakly_entities[annotator_name].append(EntitySpan(start_offset, end_offset, label))

    def __str__(self) -> str:
        return self.text

    def export_span_labels(self) -> List[EntitySpan]:
        if self.gold_entities is not None:
            return self.gold_entities
        elif self.aggregated_entities is not None:
            return self.aggregated_entities
        return []

    def export_bio_label(self) -> List[str]:
        if self.gold_entities is not None:
            return SpanLabelsToSequenceLabelConverter.entity_spans2bio(self.tokens, self.spaces, self.gold_entities)
        elif self.aggregated_entities is not None:
            return SpanLabelsToSequenceLabelConverter.entity_spans2bio(self.tokens, self.spaces, self.aggregated_entities)
        return ["O"] * len(self.tokens)
