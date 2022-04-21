from typing import List, Tuple

from funer.entity_span import EntitySpan


def bio2entity_spans_about_token_ids(bio_label: List[str]) -> List[Tuple[int, int, str]]:
    entity_spans = []
    start_i, end_i = None, None
    prev_type = None
    for i, tag in enumerate(bio_label):
        if tag.startswith("I"):
            current_type = tag[2:]
            end_i = i
            if current_type != prev_type:
                raise ValueError
        else:
            if (prev_type is not None) and (end_i is not None):
                entity_spans.append((start_i, end_i + 1, prev_type))

            if tag.startswith("O"):
                current_type = None
            elif tag.startswith("B"):
                current_type = tag[2:]
                start_i, end_i = i, i
            else:
                raise ValueError
        prev_type = current_type

    if (prev_type is not None) and (end_i is not None):
        entity_spans.append((start_i, end_i + 1, prev_type))

    return entity_spans


class SequenceLabelToSpanLabelsConverter:
    @staticmethod
    def bio2entity_spans(tokens: List[str],
                         spaces: List[bool],
                         bio_label: List[str]) -> List[EntitySpan]:
        sequence_spans = bio2entity_spans_about_token_ids(bio_label)
        span_labels = []

        for sequence_span in sequence_spans:
            start_token_i, end_token_i, label = sequence_span

            start_i = len("".join(tokens[:start_token_i])) + sum(spaces[:start_token_i])
            end_i = start_i + len("".join(tokens[start_token_i:end_token_i])) + sum(spaces[start_token_i:end_token_i - 1])

            span_labels.append(EntitySpan(start_i, end_i, label))
        return span_labels
