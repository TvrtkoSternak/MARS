if check_pairing(pairing_vars) and len(pairing_vars) % 2 == 0:
    for pair in pairing_vars:
        calculate_spin(pair)
elif check_pairing(pairing_vars):
    for i, pair in enumerate(pairing_vars):
        if i % 2 == 0:
            calculate_spin(pair)