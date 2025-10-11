import os

env = os.getenv("SECRET_KEY", 1)  # [invalid-envvar-default]
env = os.environ.get("SECRET_KEY", 1)  # [invalid-envvar-default]
