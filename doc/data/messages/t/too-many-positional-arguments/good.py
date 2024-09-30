def calculate_drag_force(*, velocity, area, density, drag_coefficient):
    return 0.5 * drag_coefficient * density * area * velocity**2


drag_force = calculate_drag_force(
    velocity=30, area=2.5, density=1.225, drag_coefficient=0.47
)
