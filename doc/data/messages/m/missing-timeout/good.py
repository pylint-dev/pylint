import requests

requests.post("http://localhost", timeout=10)

session = requests.Session()
session.post("http://localhost", timeout=10)
