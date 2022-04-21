import collections
import copy
from typing import List

from funer.converters.sequence_label_to_span_labels_converter import \
    SequenceLabelToSpanLabelsConverter
from funer.converters.span_labels_to_sequence_label_converter import \
    SpanLabelsToSequenceLabelConverter
from funer.document import Document

NO_ENTITY_LABEL = "-"


class MajorityVotingAggregator:
    def aggregate(self,
                  documents: List[Document]) -> List[Document]:
        new_documents = []
        for document in documents:
            bio_label = []
            weakly_labels = [
                SpanLabelsToSequenceLabelConverter.entity_spans2bio(document.tokens, document.spaces, weakly_entity, NO_ENTITY_LABEL)
                for weakly_entity in document.weakly_entities.values()]
            for token_i in range(len(document.tokens)):
                counter = collections.Counter([weakly_labels[label_i][token_i] for label_i in range(len(weakly_labels))])
                most_label = "O"
                for label, _ in counter.most_common():
                    if label != NO_ENTITY_LABEL and label != "O":
                        most_label = label
                        break
                bio_label.append(most_label)
            new_document = copy.deepcopy(document)
            new_document.aggregated_entities = \
                SequenceLabelToSpanLabelsConverter.bio2entity_spans(new_document.tokens, new_document.spaces, bio_label)
            new_documents.append(new_document)
        return new_documents
