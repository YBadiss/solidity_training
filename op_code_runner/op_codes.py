# extracted from https://www.evm.codes/?fork=merge with some bad JS code

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
