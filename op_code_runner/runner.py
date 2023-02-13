import copy
from tabulate import tabulate

from memory import Memory, Slot
from command import Command


def run(commands: list[Command], original_memory: Memory):
    """
    >>> run(
    ...     [Command(name='PUSH', number=2, arg='0102'), Command(name='DUP', number=1, arg=''), Command(name='DUP', number=3, arg='')],
    ...     Memory([10, 20], [])
    ... )
    (Memory(stack=[10, 258, 258, 10, 20], slots={}), 9)
    """
    all_gas_used = 0
    memory = original_memory
    for command in commands:
        memory, gas_used = run_command(command, memory, original_memory)
        all_gas_used += gas_used
    return memory, all_gas_used


def run_command(command: Command, memory: Memory, original_memory: Memory):
    new_memory = execute(command, memory)
    gas = command.gas_used(
        before=memory,
        after=new_memory,
        original=original_memory,
    )
    return new_memory, gas


def execute(command: Command, memory: Memory):
    """
    >>> execute(Command('DUP', 1, ''), Memory([10, 20], []))
    Memory(stack=[10, 10, 20], slots={})
    >>> execute(Command('DUP', 2, ''), Memory([10, 20], []))
    Memory(stack=[20, 10, 20], slots={})
    >>> execute(Command('PUSH', 2, '0102'), Memory([10, 20], []))
    Memory(stack=[258, 10, 20], slots={})
    >>> execute(Command('POP', 0, ''), Memory([10, 20], []))
    Memory(stack=[20], slots={})
    >>> execute(Command('EXP', 0, ''), Memory([3, 4], []))
    Memory(stack=[81], slots={})
    >>> execute(Command('MUL', 0, ''), Memory([4, 3, 2], []))
    Memory(stack=[12, 2], slots={})
    >>> execute(Command('OR', 0, ''), Memory([4, 3, 1], []))
    Memory(stack=[7, 1], slots={})
    >>> execute(Command('OR', 0, ''), Memory([10, 2, 1], []))
    Memory(stack=[10, 1], slots={})
    >>> execute(Command('AND', 0, ''), Memory([4, 3, 1], []))
    Memory(stack=[0, 1], slots={})
    >>> execute(Command('AND', 0, ''), Memory([10, 2, 1], []))
    Memory(stack=[2, 1], slots={})
    >>> execute(Command('SWAP', 1, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[20, 10, 30, 40, 50], slots={})
    >>> execute(Command('SWAP', 2, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[30, 20, 10, 40, 50], slots={})
    >>> execute(Command('SWAP', 3, ''), Memory([10, 20, 30, 40, 50], []))
    Memory(stack=[40, 20, 30, 10, 50], slots={})
    >>> execute(Command('NOT', 0, ''), Memory([3, 4], []))
    Memory(stack=[115792089237316195423570985008687907853269984665640564039457584007913129639932, 4], slots={})
    >>> execute(Command('SLOAD', 0, ''), Memory([1, 2], [Slot(10), Slot(20)]))
    Memory(stack=[20, 2], slots={0: Slot(value=0xa), 1: Slot(value=0x14)})
    >>> execute(Command('SSTORE', 0, ''), Memory([1, 2], [Slot(10), Slot(20)]))
    Memory(stack=[], slots={0: Slot(value=0xa), 1: Slot(value=0x2)})
    >>> execute(Command('SSTORE', 0, ''), Memory([4, 1], [Slot(10), Slot(20)]))
    Memory(stack=[], slots={0: Slot(value=0xa), 1: Slot(value=0x14), 4: Slot(value=0x1)})
    >>> execute(Command('DEADBEEF', 0, ''), Memory([2, 1], [Slot(10), Slot(20)]))
    Traceback (most recent call last):
        ...
    Exception: Unknown command Command(name='DEADBEEF', number=0, arg='')
    """
    stack = copy.deepcopy(memory.stack)
    slots = copy.deepcopy(memory.slots)

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
            slot_value = slots[stack[0]].value
            slots[stack[0]] = Slot(value=slot_value, is_warm=True)
            stack = [slot_value] + stack[1:]
        case "SSTORE":                
            slots[stack[0]] = Slot(value=stack[1], is_warm=True)
            stack = stack[2:]
        case _:
            raise Exception(f"Unknown command {command}")
    
    return Memory(stack=stack, slots=slots)


def compare(command_sets: list[str], stack: list[int], slots: list[int] | dict[int, int]):
    original_memory = Memory(stack=stack, slots=slots)
    results = [
        (i, *run(commands=Command.parse(command_set), original_memory=original_memory))
        for i, command_set in enumerate(command_sets)
    ]
    results = [
        (
            i,
            results[0][1].diff(memory),
            gas_used,
            round((gas_used - results[0][2]) / results[0][2] * 100, 2),
        )
        for i, memory, gas_used in results
    ]
    print(
        tabulate(
            results,
            headers=["Set #", "Memory", "Gas Used", "Gas Change %"],
            tablefmt="fancy_grid"
        )
    )
