from dataclasses import dataclass


@dataclass
class EntitySpan:
    start_offset: int
    end_offset: int
    label: str

    def __post_init__(self) -> None:
        if self.end_offset < self.start_offset:
            raise ValueError

    def __len__(self) -> int:
        return self.end_offset - self.start_offset + 1
