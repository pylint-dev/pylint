import requests

requests.post("http://localhost")  # [missing-timeout]

session = requests.Session()
session.post("http://localhost")  # [missing-timeout]
