from typing import List, Optional


def is_same_entity(label: Optional[str], next_label: Optional[str]):
    if label in ["O", None]:
        return False
    if next_label in ["O", None]:
        return False

    prefix, entity_type = label.split("-")  # type: ignore
    next_prefix, next_entity_type = next_label.split("-")  # type: ignore
    if entity_type != next_entity_type:
        return False

    if prefix == "B":
        if next_prefix == "B":
            return False
        else:
            return True
    else:
        if next_prefix == "B":
            return False
        else:
            return True


class SequenceLabelToSequenceLabelConverter:
    @staticmethod
    def bio2bilou(bio_labels: List[str]) -> List[str]:
        length = len(bio_labels)
        bilou_labels = ["O"] * length

        for i in range(length):
            currnet_label = bio_labels[i]
            if i == 0:
                prev_label = None
            else:
                prev_label = bio_labels[i - 1]
            if i == (length - 1):
                next_label = None
            else:
                next_label = bio_labels[i + 1]

            # currnet_label is non entity
            if currnet_label == "O":
                continue

            # currnet_label is entity
            if is_same_entity(prev_label, currnet_label):
                if is_same_entity(currnet_label, next_label):
                    bilou_labels[i] = f"I-{currnet_label[2:]}"
                else:
                    bilou_labels[i] = f"L-{currnet_label[2:]}"
            else:
                if is_same_entity(currnet_label, next_label):
                    bilou_labels[i] = f"B-{currnet_label[2:]}"
                else:
                    bilou_labels[i] = f"U-{currnet_label[2:]}"
        return bilou_labels

    @staticmethod
    def bilou2bio(bilou_labels: List[str]) -> List[str]:
        bio_labels = ["O"] * len(bilou_labels)
        for i, bilou_label in enumerate(bilou_labels):
            if bilou_label == "O":
                continue
            prefix, label = bilou_label.split("-")
            if prefix == "U":
                bio_labels[i] = f"B-{label}"
            elif prefix == "B":
                bio_labels[i] = f"B-{label}"
            elif prefix == "I":
                bio_labels[i] = f"I-{label}"
            elif prefix == "L":
                bio_labels[i] = f"I-{label}"
            else:
                raise ValueError
        return bio_labels
