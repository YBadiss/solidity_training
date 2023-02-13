from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Slot:
    value: int
    is_warm: bool = False

    @staticmethod
    def slots_from_dict(d: dict[int, "Slot"]):
        return defaultdict(lambda: Slot(0), d)

    @staticmethod
    def slots_from_list(l: list["Slot"]):
        return defaultdict(
            lambda: Slot(0),
            {i: s if isinstance(s, Slot) else Slot(s) for i, s in enumerate(l)}
        )


@dataclass
class Memory:
    stack: list[int]
    slots: dict[int, Slot]

    def __post_init__(self):
        if type(self.slots) == dict:
            self.slots = Slot.slots_from_dict(self.slots)
        elif type(self.slots) == list:
            self.slots = Slot.slots_from_list(self.slots)

    def print_stack(self):
        print(f"[{', '.join(hex(_) for _ in self.stack)}]")

    def __repr__(self) -> str:
        return f"Memory(stack={self.stack}, slots={dict(self.slots)})"
