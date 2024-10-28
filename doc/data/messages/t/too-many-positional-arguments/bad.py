# +1: [too-many-positional-arguments]
def calculate_drag_force(velocity, area, density, drag_coefficient):
    """By default, a function is 'Positional or Keyword' for all args."""
    return 0.5 * drag_coefficient * density * area * velocity**2


drag_force = calculate_drag_force(30, 2.5, 1.225, 0.47)
