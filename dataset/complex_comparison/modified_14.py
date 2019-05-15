x_more_than_max = x > maximum
y_less_than_max = y < maximum
z_more_than_min = z > minimum

if x_more_than_max and y_less_than_max and z_more_than_min:
    z += 1
    x -= 1
    y = recalculate(x, z)