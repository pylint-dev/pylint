import requests


def fetch_data():
    for i in range(1, 6):
        print(f"Attempt {i}...")
        try:
            return requests.get("https://example.com/data")
        except requests.exceptions.RequestException:
            pass
