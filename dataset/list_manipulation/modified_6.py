tuple_vals = [(unpacked_1, unpacked_2) for unpacked_1, unpacked_2 in tuple_values if unpacked_1 < 4]
for unpacked_1, unpacked_2 in tuple_vals:
    if unpacked_1 < 4:
        a.remove((unpacked_1, unpacked_2))