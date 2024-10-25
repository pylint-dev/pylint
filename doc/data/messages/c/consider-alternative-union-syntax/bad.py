from typing import Optional, Union


def forecast(
    temp: Union[int, float], unit: Optional[str]
) -> None:  # [consider-alternative-union-syntax]
    print(f'Temperature: {temp}{unit or ""}')
