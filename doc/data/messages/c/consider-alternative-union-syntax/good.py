def forecast(temp: int | float, unit: str | None) -> None:
    print(f'Temperature: {temp}{unit or ""}')
