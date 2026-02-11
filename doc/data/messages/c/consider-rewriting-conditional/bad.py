def is_penguin(animal):
    # Penguins are the only flightless, kneeless sea birds
    return animal.is_seabird() and (
        # +1: [consider-rewriting-conditional]
        not animal.can_fly()
        or not animal.has_visible_knee()
    )
