# funer

`funer` is Rule based Named Entity Recognition tool.

With `funer`, you can do the following:

- Create rule based NER model.
- Improve the rule and labeled data by comparing both.
- Labeling data with labeling functioins. 

## Example

- [Quick Example](./examples/example.ipynb)
- [Quick Example [JP]](/examples/example_jp.ipynb)

## Install

```sh
pip install funer
```

## How to use

Create Document.

```python
from funer.document import Document
import spacy

# Create documents
nlp = spacy.load("en_core_web_sm")

labeled_document_1 = Document.from_spacy_doc(
    nlp("Donald John Trump was born in New York."),
    gold_entities=[
        (0, 17, "PER"), # Donald John Trump
        (30, 38, "LOC") # New York
    ]
)
labeled_document_2 = Document.from_spacy_doc(
    nlp("Abe Rosenthal was editor-in-chief of the New York Times in 1998."),
    gold_entities=[
        (0, 13, "PER"),   # Abe Rosenthal
        (41, 55, "ORG"),  # New York Times
        (59, 63, "DATE"), # 1998
    ]
)
nolabeled_document = Document.from_spacy_doc(
    nlp("I want to go to New York."),
)
documents = [labeled_document_1, labeled_document_2, nolabeled_document]

## Option: Tokenized
tokenized_labeled_document_1 = Document(
    tokens=['Donald', 'John', 'Trump', 'was', 'born', 'in', 'New', 'York', '.'],
    spaces=[True, True, True, True, True, True, True, False, False],
    gold_label=['B-PER', 'I-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O'],
)
```

Define Labeling Functions.

```python
from funer.annotators.dictionary_annotator import DictionaryAnnotator
from funer.annotators.token_condition_annotator import (
    TokensConditionAnnotator, generate_token_conditions_function)
from funer.annotators.span_condition_annotator import SpanConditionAnnotator

# Labeling functions
## Define  Labeling Functions

# f1: Per-token labeling function
def detect_name(tokens):
    for i in range(len(tokens) - 3):
        if tokens[i:i + 3] == ["Donald", "John", "Trump"]:
            yield i, i + 3
f1 = TokensConditionAnnotator(
    name="person_f",
    f=detect_name,
    label="PER"
)

# f2: Per-token labeling function using generate_token_conditions_function
f2 = TokensConditionAnnotator(
    name="year_f",
    f=generate_token_conditions_function([
        lambda token_1: re.search(r"(19|20)\d{2}", token_1) is not None,
    ]),
    label="DATE"
)

# f3: Per-character labeling functions
def span_condition_function(text: str):
    for m in re.finditer(r"Abe Rosenthal", text):
        yield m.start(), m.end()
f3 = SpanConditionAnnotator(
    name="person_f2",
    f=span_condition_function,
    label="PER"
)


# f4: Labeling functions with dictionary
#   : (Note) Example of mistakenly extracting New York of New York Times as LOC
loc_dictionary = ["New York", "Minneapolis"]
f4 = DictionaryAnnotator(
    name="city_f",
    words=loc_dictionary,
    label="LOC"
)
```

Apply labeling functions to documents.

```python
from funer.labeling_function_applier import LabelingFunctionApplier
from funer.aggregators.majority_voting_aggregators import MajorityVotingAggregator
from funer.utils import show_labels

# Apply of labeling functions
lf_applier = LabelingFunctionApplier(lfs=[f1, f2, f3, f4])
documents = lf_applier.apply(documents)

# Integration of labeling results
aggregator = MajorityVotingAggregator()
documents = aggregator.aggregate(documents)

# Output Results
print(show_labels(documents[0]))
# > tokens       Donald   John    Trump   was   born   in   New     York    .
# > =========================================================================
# > gold_label   B-PER    I-PER   I-PER   O     O      O    B-LOC   I-LOC   O
# > -------------------------------------------------------------------------
# > person_f     B-PER    I-PER   I-PER   O     O      O    O       O       O
# > city_f       O        O       O       O     O      O    B-LOC   I-LOC   O
# > -------------------------------------------------------------------------
# > aggregate    B-PER    I-PER   I-PER   O     O      O    B-LOC   I-LOC   O

# Show stats
print(lf_applier.show_stats())
# > f_name    | pos | neg | hit
# > ==========+=====+=====+====
# > person_f  | 1   | 0   | 1  
# > year_f    | 1   | 0   | 1  
# > person_f2 | 1   | 0   | 1  
# > city_f    | 1   | 1   | 2  

# Get label
print(documents[0].export_bio_label())
# > ['B-PER', 'I-PER', 'I-PER', 'O', 'O', 'O', 'B-LOC', 'I-LOC', 'O']
```