from typing import Optional, Union


def forecast(
    temp: Union[int, float],  # [consider-alternative-union-syntax]
    unit: Optional[str],  # [consider-alternative-union-syntax]
) -> None:
    print(f'Temperature: {temp}{unit or ""}')
