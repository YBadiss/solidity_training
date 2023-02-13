import copy
from tabulate import tabulate

from memory import Memory, Slot
from command import Command


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


def compare(command_sets: list[str], stack: list[int], slots: list[int] | dict[int, int]):
    initial_memory = Memory(stack=stack, slots=slots)
    results = [
        (i, *run(commands=Command.parse(command_set), memory=initial_memory))
        for i, command_set in enumerate(command_sets)
    ]
    results = [
        (
            i,
            "-- Same --" if memory == results[0][1] else memory,
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
