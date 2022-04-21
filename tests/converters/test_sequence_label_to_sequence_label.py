from funer.converters.sequence_label_to_sequence_label import \
    SequenceLabelToSequenceLabelConverter


def test_bilou2bio():
    # bilou: ['U-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'L-ORG', 'O']
    # bio  : ['B-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'O']
    bilou_labels = ['U-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'L-ORG', 'O']
    assert ['B-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'O'] == SequenceLabelToSequenceLabelConverter.bilou2bio(bilou_labels)


def test_bio2bilou():
    # bio  : ['B-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'O']
    # bilou: ['U-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'L-ORG', 'O']
    bio_labels = ['B-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'I-ORG', 'O']
    assert ['U-PER', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'L-ORG', 'O'] == SequenceLabelToSequenceLabelConverter.bio2bilou(bio_labels)

    # bio  : ['B-PER']
    # bilou: ['U-PER']
    bio_labels = ['B-PER']
    assert ['U-PER'] == SequenceLabelToSequenceLabelConverter.bio2bilou(bio_labels)

    # bio  : ['B-PER', 'B-LOC', 'B-ORG', 'I-ORG', 'I-ORG', 'B-LOC', 'I-LOC', 'O', 'B-LOC']
    # bilou: ['U-PER', 'U-LOC', 'B-ORG', 'I-ORG', 'L-ORG', 'B-LOC', 'L-LOC', 'O', 'U-LOC']
    bio_labels = ['B-PER', 'B-LOC', 'B-ORG', 'I-ORG', 'I-ORG', 'B-LOC', 'I-LOC', 'O', 'B-LOC']
    assert ['U-PER', 'U-LOC', 'B-ORG', 'I-ORG', 'L-ORG', 'B-LOC', 'L-LOC', 'O', 'U-LOC'] == \
        SequenceLabelToSequenceLabelConverter.bio2bilou(bio_labels)

    # bio  : ['B-PER', 'B-PER', 'B-PER']
    # bilou: ['U-PER', 'U-PER', 'U-PER']
    bio_labels = ['B-PER', 'B-PER', 'B-PER']
    assert ['U-PER', 'U-PER', 'U-PER'] == SequenceLabelToSequenceLabelConverter.bio2bilou(bio_labels)
