pairing_true = check_pairing(pairing_vars)
pairs_even = len(pairing_vars) % 2 == 0

if pairing_true and pairs_even:
    for pair in pairing_vars:
        calculate_spin(pair)
elif pairing_true:
    for i, pair in enumerate(pairing_vars):
        if i % 2 == 0:
            calculate_spin(pair)