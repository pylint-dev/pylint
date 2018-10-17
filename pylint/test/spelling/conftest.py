def pytest_addoption(parser):
    parser.addoption("--spelling-dict-name", action="store")
    parser.addoption("--spelling-dict-paths", action="store")
