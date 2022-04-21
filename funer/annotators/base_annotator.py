from abc import abstractmethod

from funer.document import Document


class BaseAnnotator:
    def __init__(self,
                 name: str,
                 label: str) -> None:
        self.name = name
        self.label = label

    @abstractmethod
    def match(self,
              document: Document) -> Document:
        raise NotImplementedError
