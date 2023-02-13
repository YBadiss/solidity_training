# extracted from https://www.evm.codes/?fork=merge with some bad JS code

from gas_computation import sload_gas, sstore_gas


OP_CODES = {
    "STOP": {
        "gas": 0,
    },
    "ADD": {
        "gas": 3,
    },
    "MUL": {
        "gas": 5,
    },
    "SUB": {
        "gas": 3,
    },
    "DIV": {
        "gas": 5,
    },
    "SDIV": {
        "gas": 5,
    },
    "MOD": {
        "gas": 5,
    },
    "SMOD": {
        "gas": 5,
    },
    "ADDMOD": {
        "gas": 8,
    },
    "MULMOD": {
        "gas": 8,
    },
    "EXP": {
        "gas": 10,
    },
    "SIGNEXTEND": {
        "gas": 5,
    },
    "LT": {
        "gas": 3,
    },
    "GT": {
        "gas": 3,
    },
    "SLT": {
        "gas": 3,
    },
    "SGT": {
        "gas": 3,
    },
    "EQ": {
        "gas": 3,
    },
    "ISZERO": {
        "gas": 3,
    },
    "AND": {
        "gas": 3,
    },
    "OR": {
        "gas": 3,
    },
    "XOR": {
        "gas": 3,
    },
    "NOT": {
        "gas": 3,
    },
    "BYTE": {
        "gas": 3,
    },
    "SHL": {
        "gas": 3,
    },
    "SHR": {
        "gas": 3,
    },
    "SAR": {
        "gas": 3,
    },
    "SHA3": {
        "gas": 30,
    },
    "ADDRESS": {
        "gas": 2,
    },
    "BALANCE": {
        "gas": 100,
    },
    "ORIGIN": {
        "gas": 2,
    },
    "CALLER": {
        "gas": 2,
    },
    "CALLVALUE": {
        "gas": 2,
    },
    "CALLDATALOAD": {
        "gas": 3,
    },
    "CALLDATASIZE": {
        "gas": 2,
    },
    "CALLDATACOPY": {
        "gas": 3,
    },
    "CODESIZE": {
        "gas": 2,
    },
    "CODECOPY": {
        "gas": 3,
    },
    "GASPRICE": {
        "gas": 2,
    },
    "EXTCODESIZE": {
        "gas": 100,
    },
    "EXTCODECOPY": {
        "gas": 100,
    },
    "RETURNDATASIZE": {
        "gas": 2,
    },
    "RETURNDATACOPY": {
        "gas": 3,
    },
    "EXTCODEHASH": {
        "gas": 100,
    },
    "BLOCKHASH": {
        "gas": 20,
    },
    "COINBASE": {
        "gas": 2,
    },
    "TIMESTAMP": {
        "gas": 2,
    },
    "NUMBER": {
        "gas": 2,
    },
    "PREVRANDAO": {
        "gas": 2,
    },
    "GASLIMIT": {
        "gas": 2,
    },
    "CHAINID": {
        "gas": 2,
    },
    "SELFBALANCE": {
        "gas": 5,
    },
    "BASEFEE": {
        "gas": 2,
    },
    "POP": {
        "gas": 2,
    },
    "MLOAD": {
        "gas": 3,
    },
    "MSTORE": {
        "gas": 3,
    },
    "SLOAD": {
        "gas": sload_gas,
    },
    "SSTORE": {
        "gas": sstore_gas,
    },
    "JUMP": {
        "gas": 8,
    },
    "JUMPI": {
        "gas": 10,
    },
    "PC": {
        "gas": 2,
    },
    "MSIZE": {
        "gas": 2,
    },
    "GAS": {
        "gas": 2,
    },
    "JUMPDEST": {
        "gas": 1,
    },
    "PUSH": {
        "gas": 3,
    },
    "DUP": {
        "gas": 3,
    },
    "SWAP": {
        "gas": 3,
    },
    "LOG": {
        "gas": 375,
    },
    "CREATE": {
        "gas": 32000,
    },
    "CALL": {
        "gas": 100,
    },
    "CALLCODE": {
        "gas": 100,
    },
    "RETURN": {
        "gas": 0,
    },
    "DELEGATECALL": {
        "gas": 100,
    },
    "CREATE2": {
        "gas": 32000,
    },
    "STATICCALL": {
        "gas": 100,
    },
    "REVERT": {
        "gas": 0,
    },
    "INVALID": {
        "gas": 0,
    },
    "SELFDESTRUCT": {
        "gas": 5000,
    }
}
