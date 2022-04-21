
from funer.aggregators.majority_voting_aggregators import \
    MajorityVotingAggregator
from funer.document import Document
from funer.entity_span import EntitySpan
from funer.utils import show_labels


def test_show_labels():
    # all
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
    assert """tokens       Michael   Jackson   was   born   in   Gary    in   1958     .
==========================================================================
gold_label   B-PER     I-PER     O     O      O    B-LOC   O    B-DATE   O
--------------------------------------------------------------------------
f1           B-PER     I-PER     O     O      O    O       O    O        O
f2           O         O         O     O      O    B-LOC   O    O        O
f3           O         O         O     O      O    O       O    B-DATE   O
--------------------------------------------------------------------------
aggregate    B-PER     I-PER     O     O      O    B-LOC   O    B-DATE   O""" == show_labels(document)

    # no gold_label
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 15, "PER")]
    document.weakly_entities["f2"] = [EntitySpan(28, 32, "LOC")]
    document.weakly_entities["f3"] = [EntitySpan(36, 40, "DATE")]

    aggregator = MajorityVotingAggregator()
    [document] = aggregator.aggregate([document])
    assert """tokens       Michael   Jackson   was   born   in   Gary    in   1958     .
==========================================================================
gold_label   -         -         -     -      -    -       -    -        -
--------------------------------------------------------------------------
f1           B-PER     I-PER     O     O      O    O       O    O        O
f2           O         O         O     O      O    B-LOC   O    O        O
f3           O         O         O     O      O    O       O    B-DATE   O
--------------------------------------------------------------------------
aggregate    B-PER     I-PER     O     O      O    B-LOC   O    B-DATE   O""" == show_labels(document)

    # no aggregate
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 15, "PER")]
    document.weakly_entities["f2"] = [EntitySpan(28, 32, "LOC")]
    document.weakly_entities["f3"] = [EntitySpan(36, 40, "DATE")]
    assert """tokens       Michael   Jackson   was   born   in   Gary    in   1958     .
==========================================================================
gold_label   -         -         -     -      -    -       -    -        -
--------------------------------------------------------------------------
f1           B-PER     I-PER     O     O      O    O       O    O        O
f2           O         O         O     O      O    B-LOC   O    O        O
f3           O         O         O     O      O    O       O    B-DATE   O""" == show_labels(document)

    # no function label
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
    )

    aggregator = MajorityVotingAggregator()
    [document] = aggregator.aggregate([document])
    assert """tokens       Michael   Jackson   was   born   in   Gary   in   1958   .
=======================================================================
gold_label   -         -         -     -      -    -      -    -      -
-----------------------------------------------------------------------
aggregate    O         O         O     O      O    O      O    O      O""" == show_labels(document)


def test_show_labels_without_gl():
    document = Document(
        tokens=['Michael', 'Jackson', 'was', 'born', 'in', 'Gary', 'in', '1958', '.'],
        spaces=[True, True, True, True, True, True, True, False, False],
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 15, "PER")]
    document.weakly_entities["f2"] = [EntitySpan(28, 32, "LOC")]
    document.weakly_entities["f3"] = [EntitySpan(36, 40, "DATE")]

    aggregator = MajorityVotingAggregator()
    [document] = aggregator.aggregate([document])
    show_labels(document)


def test_show_labels_jp():
    document = Document(
        tokens=["東京", "出身", "の", "吉田", "は", "4", "月", "から", "JR", "で", "働く", "。"],
        gold_label=["B-LOC", "O", "O", "B-PER", "O", "B-DATE", "I-DATE", "O", "B-ORG", "O", "O", "O"]
    )

    document.weakly_entities["f1"] = [EntitySpan(0, 2, "LOC")]

    aggregator = MajorityVotingAggregator()
    [document] = aggregator.aggregate([document])
    assert """tokens       東京    出身   の   吉田    は   4        月       から   JR      で   働く   。
=============================================================================================
gold_label   B-LOC   O      O    B-PER   O    B-DATE   I-DATE   O      B-ORG   O    O      O 
---------------------------------------------------------------------------------------------
f1           B-LOC   O      O    O       O    O        O        O      O       O    O      O 
---------------------------------------------------------------------------------------------
aggregate    B-LOC   O      O    O       O    O        O        O      O       O    O      O """ == show_labels(document)
