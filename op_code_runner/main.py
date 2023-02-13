from command import Command
from memory import Memory, Slot
from runner import run


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