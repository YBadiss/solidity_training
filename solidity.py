from dataclasses import dataclass
import re
from typing import Optional

COMMANDS: list[str] = ["STOP","ADD","MUL","SUB","DIV","SDIV","MOD","SMOD","ADDMOD","MULMOD","EXP","SIGNEXTEND","LT","GT","SLT","SGT","EQ","ISZERO","AND","OR","XOR","NOT","BYTE","SHL","SHR","SAR","SHA3","ADDRESS","BALANCE","ORIGIN","CALLER","CALLVALUE","CALLDATALOAD","CALLDATASIZE","CALLDATACOPY","CODESIZE","CODECOPY","GASPRICE","EXTCODESIZE","EXTCODECOPY","RETURNDATASIZE","RETURNDATACOPY","EXTCODEHASH","BLOCKHASH","COINBASE","TIMESTAMP","NUMBER","PREVRANDAO","GASLIMIT","CHAINID","SELFBALANCE","BASEFEE","POP","MLOAD","MSTORE","SLOAD","SSTORE","JUMP","JUMPI","PC","MSIZE","GAS","JUMPDEST","PUSH","DUP","SWAP","LOG","CREATE","CALL","CALLCODE","RETURN","DELEGATECALL","STATICCALL","REVERT","INVALID","SELFDESTRUCT"]
COMMANDS_REGEX = f"(?P<name>{'|'.join(COMMANDS)})(?P<number>\\d+)?( (?P<arg>.+))?"


@dataclass
class Command:
    name: str
    number: int
    arg: str


@dataclass
class Memory:
    stack: list[int]
    slots: list[int]

    def print_stack(self):
        print(f"[{', '.join(hex(_) for _ in self.stack)}]")


def parse_command(line: str) -> Command:
    """
    >>> parse_command("070 DUP1 - LINE 12")
    Command(name='DUP', number=1, arg='')
    >>> parse_command("071 PUSH2 0102 - LINE 12")
    Command(name='PUSH', number=2, arg='0102')
    >>> parse_command("071 SLOAD - LINE 12")
    Command(name='SLOAD', number=0, arg='')
    """
    m = re.match(f"(.+)?{COMMANDS_REGEX} -", line)
    return Command(m["name"], int(m["number"] or 0), m["arg"] or "")


def run_command(command: Command, memory: Memory):
    """
    >>> run_command(Command('DUP', 1, ''), Memory([10, 20], []))
    Memory(stack=[10, 10, 20], slots=[])
    >>> run_command(Command('DUP', 2, ''), Memory([10, 20], []))
    Memory(stack=[20, 10, 20], slots=[])
    >>> run_command(Command('PUSH', 2, '0102'), Memory([10, 20], []))
    Memory(stack=[258, 10, 20], slots=[])
    >>> run_command(Command('POP', 0, ''), Memory([10, 20], []))
    Memory(stack=[20], slots=[])
    >>> run_command(Command('EXP', 0, ''), Memory([3, 4], []))
    Memory(stack=[81], slots=[])
    >>> run_command(Command('MUL', 0, ''), Memory([4, 3, 2], []))
    Memory(stack=[12, 2], slots=[])
    >>> run_command(Command('OR', 0, ''), Memory([4, 3, 1], []))
    Memory(stack=[7, 1], slots=[])
    >>> run_command(Command('OR', 0, ''), Memory([10, 2, 1], []))
    Memory(stack=[10, 1], slots=[])
    >>> run_command(Command('AND', 0, ''), Memory([4, 3, 1], []))
    Memory(stack=[0, 1], slots=[])
    >>> run_command(Command('AND', 0, ''), Memory([10, 2, 1], []))
    Memory(stack=[2, 1], slots=[])
    >>> run_command(Command('SWAP', 1, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[20, 10, 30, 40, 50], slots=[])
    >>> run_command(Command('SWAP', 2, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[30, 20, 10, 40, 50], slots=[])
    >>> run_command(Command('SWAP', 3, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[40, 20, 30, 10, 50], slots=[])
    >>> run_command(Command('NOT', 0, ''), Memory([3, 4], []))
    Memory(stack=[115792089237316195423570985008687907853269984665640564039457584007913129639932, 4], slots=[])
    >>> run_command(Command('SLOAD', 0, ''), Memory([2, 1], [10, 20]))
    Memory(stack=[20, 1], slots=[10, 20])
    >>> run_command(Command('SSTORE', 0, ''), Memory([2, 1], [10, 20]))
    Memory(stack=[], slots=[10, 1])
    >>> run_command(Command('DEADBEEF', 0, ''), Memory([2, 1], [10, 20]))
    Traceback (most recent call last):
        ...
    Exception: Unknown command Command(name='DEADBEEF', number=0, arg='')
    """
    stack = memory.stack
    slots = memory.slots
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
            stack = [slots[stack[0] - 1]] + stack[1:]
        case "SSTORE":
            slots = slots[:stack[0] - 1] + [stack[1]] + memory.slots[stack[0]:]
            stack = stack[2:]
        case _:
            raise Exception(f"Unknown command {command}")
    return Memory(stack=stack, slots=slots)



def run(command_lines: list[str], memory: Memory, debug=False):
    """
    >>> run(["071 PUSH2 0102 - LINE 12", "070 DUP1 - LINE 12", "070 DUP3 - LINE 12"], Memory([10, 20], []), debug=True)
    [0xa, 0x14]
    > Command(name='PUSH', number=2, arg='0102')
    [0x102, 0xa, 0x14]
    > Command(name='DUP', number=1, arg='')
    [0x102, 0x102, 0xa, 0x14]
    > Command(name='DUP', number=3, arg='')
    [0xa, 0x102, 0x102, 0xa, 0x14]
    Memory(stack=[10, 258, 258, 10, 20], slots=[])
    """
    if debug:
        memory.print_stack()
    for command_line in command_lines:
        command = parse_command(command_line)
        if debug:
            print(f"> {command}")
        memory = run_command(command, memory)
        if debug:
            memory.print_stack()
    return memory


run(
    [
        "070 DUP1 - LINE 12",
        "071 PUSH1 00 - LINE 12",
        "073 DUP1 - LINE 12",
        "074 PUSH2 0100 - LINE 12",
        "077 EXP - LINE 12",
        "078 DUP2 - LINE 12",
        "079 SLOAD - LINE 12",
        "080 DUP2 - LINE 12",
        "081 PUSH4 ffffffff - LINE 12",
        "086 MUL - LINE 12",
        "087 NOT - LINE 12",
        "088 AND - LINE 12",
        "089 SWAP1 - LINE 12",
        "090 DUP4 - LINE 12",
        "091 PUSH4 ffffffff - LINE 12",
        "096 AND - LINE 12",
        "097 MUL - LINE 12",
        "098 OR - LINE 12",
        "099 SWAP1 - LINE 12",
        "100 SSTORE - LINE 12",
        "101 POP - LINE 12",
        "102 POP - LINE 12",
    ],
    Memory(
        [
            0x00000000000000000000000000000000000000000000000000000000e3cff634,
            0x0000000000000000000000000000000000000000000000000000000000000043,
            0x0000000000000000000000000000000000000000000000000000000000000005,
        ],
        [
            1,
            0,
        ],
    ),
    debug=True,
)
