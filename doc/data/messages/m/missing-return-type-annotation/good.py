def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)


async def fetch_data(url: str) -> dict:
    return await get(url)


class Calculator:
    def __init__(self, initial: int):  # __init__ doesn't need return type
        self.value = initial
