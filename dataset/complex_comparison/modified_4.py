difference_positive = calculate_difference(x, z) > 0
y_larger_z = y > z

if difference_positive and y_larger_z:
    z = y
    y = recalculate_y(z)