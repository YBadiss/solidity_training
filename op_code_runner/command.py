from dataclasses import dataclass
import re
from memory import Memory

from op_codes import OP_CODES


OP_CODES_REGEX = f"(?P<name>({'|'.join(OP_CODES.keys())}))(?P<number>\\d+)?(\\s+(?P<arg>[^- ]+))?"


@dataclass
class Command:
    name: str
    number: int
    arg: str

    def gas_used(self, before: Memory, after: Memory, original: Memory) -> int:
        gas = OP_CODES[self.name]["gas"]
        if callable(gas):
            gas = gas(before, after, original)
        return gas

    @classmethod
    def parse_line(cls, line: str):
        """
        >>> Command.parse_line("070 DUP1 - LINE 12")
        Command(name='DUP', number=1, arg='')
        >>> Command.parse_line("071 PUSH2 0102 - LINE 12")
        Command(name='PUSH', number=2, arg='0102')
        >>> Command.parse_line("071 SLOAD - LINE 12")
        Command(name='SLOAD', number=0, arg='')
        >>> Command.parse_line("SLOAD")
        Command(name='SLOAD', number=0, arg='')
        >>> Command.parse_line("NOTACODE")
        >>> Command.parse_line("")
        """
        if m := re.match(f"(.+)?{OP_CODES_REGEX}(\\s+.+$|$)", line):
            return cls(m["name"], int(m["number"] or 0), m["arg"] or "")

    @classmethod
    def parse(cls, block: str):
        """
        >>> list(Command.parse('''070 DUP1 - LINE 12
        ... 071 PUSH2 0102 - LINE 12
        ... 071 SLOAD - LINE 12'''))
        [Command(name='DUP', number=1, arg=''), Command(name='PUSH', number=2, arg='0102'), Command(name='SLOAD', number=0, arg='')]
        """
        for line in block.splitlines():
            if command := cls.parse_line(line):
                yield command
