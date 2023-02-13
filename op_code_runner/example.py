from runner import compare


# set the initial state of the stack
stack = [
    0x000000000000000000000000000000000000000000000000000000000000000b,
    0x0000000000000000000000000000000000000000000000000000000000000055,
    0x000000000000000000000000000000000000000000000000000000005220b501,
]

# set the initial state of the slots
slots = [
    0x0000000000000000000000000000000000000000000000000000000F0000000A,
    0x0000000000000000000000000000000000000000000000000000000000000000,
]
# if you have a complex slot structure, you can pass the slot ids explicitely
# slots = {
#     0: 0x0000000000000000000000000000000000000000000000000000000F0000000A,
#     1: 0x0000000000000000000000000000000000000000000000000000000000000000,
#     9: 0x0000000000000000000000000000000000000000000000000000000000000001,
# }

# sets of commands to execute on the initial memory
# the first set is considered to be the reference
command_sets = [
    """
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
    """,
    """
        DUP1
        PUSH4 ffffffff
        AND
        PUSH1 00
        SLOAD
        PUSH4 ffffffff
        NOT
        AND
        OR
        PUSH1 00
        SSTORE
        POP
        POP
    """
]

# nothing else to do for you!
# we will now run the command sets, and print a brief recap
compare(command_sets, stack, slots)
