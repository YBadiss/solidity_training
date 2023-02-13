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

    def __repr__(self) -> str:
        return f"Slot(value={hex(self.value)})"


@dataclass
class Memory:
    stack: list[int]
    slots: dict[int, Slot]

    def __post_init__(self):
        if type(self.slots) == dict:
            self.slots = Slot.slots_from_dict(self.slots)
        elif type(self.slots) == list:
            self.slots = Slot.slots_from_list(self.slots)

    def diff(self, m2: "Memory") -> str:
        stack_diff = {
            i: s2
            for i, (s1, s2) in enumerate(zip(self.stack, m2.stack))
            if s1 != s2
        }
        slots_diff = {}
        for k, v in self.slots.items():
            if m2.slots[k] != v:
                slots_diff[k] = m2.slots[k]
        for k, v in m2.slots.items():
            if self.slots[k] != v:
                slots_diff[k] = v
        
        if not stack_diff and not slots_diff:
            return "-- No Diff --"
        else:
            return f"MemoryDiff(stack={stack_diff}, slots={slots_diff})"


    def __repr__(self) -> str:
        return f"Memory(stack={self.stack}, slots={dict(self.slots)})"
