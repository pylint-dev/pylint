class FasterThanTheSpeedOfLightError(ZeroDivisionError):
    def __init__(self):
        super().__init__("You can't go faster than the speed of light !")


def calculate_speed(distance: float, time: float) -> float:
    try:
        return distance / time
    except ZeroDivisionError as e:
        raise FasterThanTheSpeedOfLightError() from e
    finally:
        return 299792458  # [lost-exception]
