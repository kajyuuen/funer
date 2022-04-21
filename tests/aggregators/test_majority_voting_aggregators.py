from funer.aggregators.majority_voting_aggregators import \
    MajorityVotingAggregator
from funer.document import Document
from funer.entity_span import EntitySpan


def test_majority_voting_aggregator():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
        gold_label=['B-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'O', 'B-DATE', 'O']
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 15, "PER")]
    document.weakly_entities["f2"] = [EntitySpan(28, 32, "LOC")]
    document.weakly_entities["f3"] = [EntitySpan(36, 40, "DATE")]

    aggregator = MajorityVotingAggregator()
    [document] = aggregator.aggregate([document])
