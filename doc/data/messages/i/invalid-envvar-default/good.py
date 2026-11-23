import os

env = os.getenv("SECRET_KEY", "1")
env = os.environ.get("SECRET_KEY", "1")
