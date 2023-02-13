from collections import defaultdict
import copy
from dataclasses import dataclass
import re


OP_CODES = {
    "STOP": {
        "gas": {
            "cold": 0,
            "warm": 0,
        }
    },
    "ADD": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "MUL": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "SUB": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "DIV": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "SDIV": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "MOD": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "SMOD": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "ADDMOD": {
        "gas": {
            "cold": 8,
            "warm": 8,
        }
    },
    "MULMOD": {
        "gas": {
            "cold": 8,
            "warm": 8,
        }
    },
    "EXP": {
        "gas": {
            "cold": 10,
            "warm": 10,
        }
    },
    "SIGNEXTEND": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "LT": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "GT": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SLT": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SGT": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "EQ": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "ISZERO": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "AND": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "OR": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "XOR": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "NOT": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "BYTE": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SHL": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SHR": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SAR": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SHA3": {
        "gas": {
            "cold": 30,
            "warm": 30,
        }
    },
    "ADDRESS": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "BALANCE": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "ORIGIN": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CALLER": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CALLVALUE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CALLDATALOAD": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "CALLDATASIZE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CALLDATACOPY": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "CODESIZE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CODECOPY": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "GASPRICE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "EXTCODESIZE": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "EXTCODECOPY": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "RETURNDATASIZE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "RETURNDATACOPY": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "EXTCODEHASH": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "BLOCKHASH": {
        "gas": {
            "cold": 20,
            "warm": 20,
        }
    },
    "COINBASE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "TIMESTAMP": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "NUMBER": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "PREVRANDAO": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "GASLIMIT": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "CHAINID": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "SELFBALANCE": {
        "gas": {
            "cold": 5,
            "warm": 5,
        }
    },
    "BASEFEE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "POP": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "MLOAD": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "MSTORE": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SLOAD": {
        "gas": {
            "cold": 2100,
            "warm": 100,
        }
    },
    "SSTORE": {
        "gas": {
            "cold": 5100,
            "warm": 3000,
        }
    },
    "JUMP": {
        "gas": {
            "cold": 8,
            "warm": 8,
        }
    },
    "JUMPI": {
        "gas": {
            "cold": 10,
            "warm": 10,
        }
    },
    "PC": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "MSIZE": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "GAS": {
        "gas": {
            "cold": 2,
            "warm": 2,
        }
    },
    "JUMPDEST": {
        "gas": {
            "cold": 1,
            "warm": 1,
        }
    },
    "PUSH": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "DUP": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "SWAP": {
        "gas": {
            "cold": 3,
            "warm": 3,
        }
    },
    "LOG": {
        "gas": {
            "cold": 375,
            "warm": 375,
        }
    },
    "CREATE": {
        "gas": {
            "cold": 32000,
            "warm": 32000,
        }
    },
    "CALL": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "CALLCODE": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "RETURN": {
        "gas": {
            "cold": 0,
            "warm": 0,
        }
    },
    "DELEGATECALL": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "CREATE2": {
        "gas": {
            "cold": 32000,
            "warm": 32000,
        }
    },
    "STATICCALL": {
        "gas": {
            "cold": 100,
            "warm": 100,
        }
    },
    "REVERT": {
        "gas": {
            "cold": 0,
            "warm": 0,
        }
    },
    "INVALID": {
        "minimum_gas": None
    },
    "SELFDESTRUCT": {
        "gas": {
            "cold": 5000,
            "warm": 5000,
        }
    }
}
OP_CODES_REGEX = f"(?P<name>({'|'.join(OP_CODES.keys())}))(?P<number>\\d+)?(\\s+(?P<arg>[^- ]+))?"


@dataclass
class Command:
    name: str
    number: int
    arg: str

    @property
    def gas_cold(self):
        return OP_CODES[self.name]["gas"]["cold"]

    @property
    def gas_warm(self):
        return OP_CODES[self.name]["gas"]["warm"]

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


@dataclass
class Slot:
    value: int
    is_warm: bool = False

    @staticmethod
    def slots_from_dict(d: dict[int, "Slot"]):
        return defaultdict(lambda: Slot(0), d)

    @staticmethod
    def slots_from_list(l: list["Slot"]):
        return defaultdict(lambda: Slot(0), {i: s for i, s in enumerate(l)})


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


def run_command(command: Command, memory: Memory):
    """
    >>> run_command(Command('DUP', 1, ''), Memory([10, 20], []))[0]
    Memory(stack=[10, 10, 20], slots={})
    >>> run_command(Command('DUP', 2, ''), Memory([10, 20], []))[0]
    Memory(stack=[20, 10, 20], slots={})
    >>> run_command(Command('PUSH', 2, '0102'), Memory([10, 20], []))[0]
    Memory(stack=[258, 10, 20], slots={})
    >>> run_command(Command('POP', 0, ''), Memory([10, 20], []))[0]
    Memory(stack=[20], slots={})
    >>> run_command(Command('EXP', 0, ''), Memory([3, 4], []))[0]
    Memory(stack=[81], slots={})
    >>> run_command(Command('MUL', 0, ''), Memory([4, 3, 2], []))[0]
    Memory(stack=[12, 2], slots={})
    >>> run_command(Command('OR', 0, ''), Memory([4, 3, 1], []))[0]
    Memory(stack=[7, 1], slots={})
    >>> run_command(Command('OR', 0, ''), Memory([10, 2, 1], []))[0]
    Memory(stack=[10, 1], slots={})
    >>> run_command(Command('AND', 0, ''), Memory([4, 3, 1], []))[0]
    Memory(stack=[0, 1], slots={})
    >>> run_command(Command('AND', 0, ''), Memory([10, 2, 1], []))[0]
    Memory(stack=[2, 1], slots={})
    >>> run_command(Command('SWAP', 1, ''), Memory([10, 20, 30, 40, 50], []))[0]
    Memory(stack=[20, 10, 30, 40, 50], slots={})
    >>> run_command(Command('SWAP', 2, ''), Memory([10, 20, 30, 40, 50], []))[0]
    Memory(stack=[30, 20, 10, 40, 50], slots={})
    >>> run_command(Command('SWAP', 3, ''), Memory([10, 20, 30, 40, 50], []))[0]
    Memory(stack=[40, 20, 30, 10, 50], slots={})
    >>> run_command(Command('NOT', 0, ''), Memory([3, 4], []))[0]
    Memory(stack=[115792089237316195423570985008687907853269984665640564039457584007913129639932, 4], slots={})
    >>> run_command(Command('SLOAD', 0, ''), Memory([1, 2], [Slot(10), Slot(20)]))[0]
    Memory(stack=[20, 2], slots={0: Slot(value=10, is_warm=False), 1: Slot(value=20, is_warm=True)})
    >>> run_command(Command('SSTORE', 0, ''), Memory([1, 2], [Slot(10), Slot(20)]))[0]
    Memory(stack=[], slots={0: Slot(value=10, is_warm=False), 1: Slot(value=2, is_warm=True)})
    >>> run_command(Command('SSTORE', 0, ''), Memory([4, 1], [Slot(10), Slot(20)]))[0]
    Memory(stack=[], slots={0: Slot(value=10, is_warm=False), 1: Slot(value=20, is_warm=False), 4: Slot(value=1, is_warm=True)})
    >>> run_command(Command('DEADBEEF', 0, ''), Memory([2, 1], [Slot(10), Slot(20)]))
    Traceback (most recent call last):
        ...
    Exception: Unknown command Command(name='DEADBEEF', number=0, arg='')
    """
    stack = copy.deepcopy(memory.stack)
    slots = copy.deepcopy(memory.slots)
    gas_used = None

    match command.name:
        case "DUP":
            stack = [stack[command.number - 1]] + stack
        case "PUSH":
            stack = [int(command.arg, 16)] + stack
        case "POP":
            stack = stack[1:]
        case "EXP":
            stack = [stack[0] ** stack[1]] + stack[2:]
        case "MUL":
            stack = [stack[0] * stack[1]] + stack[2:]
        case "OR":
            stack = [stack[0] | stack[1]] + stack[2:]
        case "AND":
            stack = [stack[0] & stack[1]] + stack[2:]
        case "SWAP":
            stack = [stack[command.number]] + stack[1:command.number] + [stack[0]] + stack[command.number + 1:]
        case "NOT":
            stack = [0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff - stack[0]] + stack[1:]
        case "SLOAD":
            if slots[stack[0]].is_warm:
                gas_used = command.gas_warm
            slot_value = slots[stack[0]].value
            slots[stack[0]] = Slot(value=slot_value, is_warm=True)
            stack = [slot_value] + stack[1:]
        case "SSTORE":
            if slots[stack[0]].is_warm:
                gas_used = command.gas_warm
            slots[stack[0]] = Slot(value=stack[1], is_warm=True)
            stack = stack[2:]
        case _:
            raise Exception(f"Unknown command {command}")

    if gas_used is None:
        gas_used = command.gas_cold 
    return Memory(stack=stack, slots=slots), gas_used



def run(commands: list[Command], memory: Memory):
    """
    >>> run(
    ...     [Command(name='PUSH', number=2, arg='0102'), Command(name='DUP', number=1, arg=''), Command(name='DUP', number=3, arg='')],
    ...     Memory([10, 20], [])
    ... )
    (Memory(stack=[10, 258, 258, 10, 20], slots={}), 9)
    """
    all_gas_used = 0
    for command in commands:
        memory, gas_used = run_command(command, memory)
        all_gas_used += gas_used
    return memory, all_gas_used


initial_memory = Memory(
    stack=[
        0x000000000000000000000000000000000000000000000000000000000000000b,
        0x0000000000000000000000000000000000000000000000000000000000000055,
        0x000000000000000000000000000000000000000000000000000000005220b501,
    ],
    slots=[
        Slot(0x0000000000000000000000000000000000000000000000000000000F0000000A),
        Slot(0x0000000000000000000000000000000000000000000000000000000000000000),
    ],
)


commands = Command.parse("""
    117 PUSH1 00 - LINE 12
    119 DUP1 - LINE 12
    120 PUSH2 0100 - LINE 12
    123 EXP - LINE 12
    124 DUP2 - LINE 12
    125 SLOAD - LINE 12
    126 DUP2 - LINE 12
    127 PUSH4 ffffffff - LINE 12
    132 MUL - LINE 12
    133 NOT - LINE 12
    134 AND - LINE 12
    135 SWAP1 - LINE 12
    136 DUP4 - LINE 12
    137 PUSH4 ffffffff - LINE 12
    142 AND - LINE 12
    143 MUL - LINE 12
    144 OR - LINE 12
    145 SWAP1 - LINE 12
    146 SSTORE - LINE 12
    147 POP - LINE 12
    148 POP - LINE 12
""")
memory1, gas_used1 = run(commands=commands, memory=initial_memory)

commands = Command.parse("""
    070 DUP1 - LINE 12
    081 PUSH4 ffffffff - LINE 12
    087 AND - LINE 12
    071 PUSH1 00 - LINE 12
    079 SLOAD - LINE 12
    081 PUSH4 ffffffff - LINE 12
    081 NOT - LINE 12
    087 AND - LINE 12
    079 OR - LINE 12
    081 PUSH1 00 - LINE 12
    079 SSTORE - LINE 12
    079 POP - LINE 12
    079 POP - LINE 12
""")
memory2, gas_used2 = run(commands=commands, memory=initial_memory)

print(f"memory1: {memory1}, gas_used1: {gas_used1}")
print(f"memory2: {memory2}, gas_used2: {gas_used2}")

assert memory1 == memory2