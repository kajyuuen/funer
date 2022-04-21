import texttable

from funer.converters.span_labels_to_sequence_label_converter import \
    SpanLabelsToSequenceLabelConverter
from funer.document import Document


def show_labels(document: Document):
    table = texttable.Texttable()
    table.set_deco(texttable.Texttable.HEADER)
    table.set_max_width(0)
    table.set_header_align(["l"] * (len(document.tokens) + 1))
    table.set_cols_dtype(["t"] * (len(document.tokens) + 1))

    table_list = []

    table_list.append(["tokens"] + document.tokens)

    # Gold Label
    if document.gold_entities is None:
        table_list.append(["gold_label"] + ["-"] * len(document.tokens))
    else:
        table_list.append(["gold_label"] + SpanLabelsToSequenceLabelConverter.entity_spans2bio(document.tokens, document.spaces, document.gold_entities))

    # Function Label
    if len(document.weakly_entities) > 0:
        for f_name, weakly_entity in document.weakly_entities.items():
            table_list.append([f_name] + SpanLabelsToSequenceLabelConverter.entity_spans2bio(document.tokens, document.spaces, weakly_entity))

    # Aggregated label
    if document.aggregated_entities is not None:
        table_list.append(["aggregate"] + SpanLabelsToSequenceLabelConverter.entity_spans2bio(document.tokens, document.spaces, document.aggregated_entities))

    table.add_rows(table_list)
    table_text = table.draw()
    split_table_text = table_text.split("\n")
    split_bar = split_table_text[1].replace("=", "-")

    result_list = split_table_text[:3]
    if len(document.weakly_entities) > 0:
        if document.aggregated_entities is not None:
            result_list += [split_bar] + split_table_text[3:-1] + [split_bar] + split_table_text[-1:]
        else:
            result_list += [split_bar] + split_table_text[3:]
    else:
        result_list += [split_bar] + split_table_text[3:]

    return "\n".join(result_list)
