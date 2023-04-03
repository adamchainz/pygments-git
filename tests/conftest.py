def pytest_addoption(parser):
    parser.addoption("--save", action="store_true", help="Save output to file")
