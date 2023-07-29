import requests


def fetch_data():
    i = 1
    while i < 6:  # [while-used]
        print(f"Attempt {i}...")
        try:
            return requests.get("https://example.com/data")
        except requests.exceptions.RequestException:
            pass
        i += 1
