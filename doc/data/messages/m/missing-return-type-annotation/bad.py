def calculate_sum(numbers: list[int]):  # [missing-return-type-annotation]
    return sum(numbers)


async def fetch_data(url: str):  # [missing-return-type-annotation]
    return await get(url)
