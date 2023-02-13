from memory import Memory


def sload_gas(before: Memory, after: Memory, original: Memory):
    """See details of computation at https://www.evm.codes/#54"""
    slot_id = before.stack[0]
    slot_before = before.slots[slot_id]

    if slot_before.is_warm:
        return 100
    else:
        return 2100


def sstore_gas(before: Memory, after: Memory, original: Memory):
    """See details of computation at https://www.evm.codes/#55"""
    slot_id = before.stack[0]
    slot_before = before.slots[slot_id]
    slot_after = after.slots[slot_id]
    slot_original = original.slots[slot_id]

    setting_new_value = slot_before.value != slot_after.value
    value_unchanged_before_transaction = slot_before.value == slot_original.value
    value_never_set = slot_original.value == 0
    
    if setting_new_value and value_unchanged_before_transaction:
        if value_never_set:
            gas = 20000
        else:
            gas = 2900
    else:
        gas = 100
    if not slot_before.is_warm:
        gas += 2100
    return gas
