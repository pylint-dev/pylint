# Pylint Development Instructions

Always follow these instructions first and fallback to additional search and context gathering only if the information in these instructions is incomplete or found to be in error.

## Working Effectively

- Bootstrap and set up the development environment:
  - `python --version` -- verify Python 3.10+ is available
  - `pip install -e .` -- install pylint in development mode (takes ~30-60 seconds)
  - `pip install coverage pytest pytest-cov pytest-xdist tox` -- install core test dependencies

- Run basic validation:
  - `pylint --help` -- verify pylint is working correctly
  - `pylint --disable=all --enable=E,F pylint/` -- run pylint on itself for errors only (takes ~20 seconds, some import errors expected)

- Run tests:
  - `pytest tests/test_check_parallel.py -v` -- run a quick test file (~2 seconds)
  - `pytest tests/test_self.py -v` -- run core functionality tests (~15 seconds)
  - `pytest tests/test_functional.py::test_functional --maxfail=5 -q` -- run functional tests (takes ~60 seconds, NEVER CANCEL, set timeout to 120+ seconds)
  - **NEVER CANCEL:** Full test suite takes 60+ seconds. Always wait for completion.

- Install additional development dependencies:
  - `pip install pre-commit` -- for code formatting and linting
  - `cd doc && pip install -r requirements.txt` -- for documentation (requires network access)

- Build documentation:
  - `cd doc && make install-dependencies` -- install doc dependencies (~10 seconds)
  - `cd doc && make html` -- build documentation (~3 minutes, NEVER CANCEL, may fail without network access)
  - **NEVER CANCEL:** Documentation build takes up to 3 minutes. Set timeout to 300+ seconds.

## Validation

- Always run pylint on your changes before committing:
  - `pylint --rcfile=pylintrc --fail-on=I path/to/your/changes.py` -- standard pylint run
  - `pylint --disable=all --enable=E,F,W path/to/your/changes.py` -- focus on errors and warnings

- Run formatting and pre-commit checks:
  - `pre-commit run --all-files` -- run all formatting checks (requires network for initial setup)
  - **Network dependency:** pre-commit may fail in isolated environments due to hook downloads

- **VALIDATION SCENARIOS:** Always test your changes by:
  - Running pylint on a sample Python file: `echo "def badFunction(): pass" > /tmp/test_sample.py && pylint --enable=C0103 /tmp/test_sample.py` (should find naming issues)
  - Verifying pylint CLI still works: `pylint --help` and `pylint --list-msgs | head -10`
  - Testing message ID functionality: `pylint --help-msg=C0103` (should show invalid-name help)
  - Checking specific module: `pylint --rcfile=pylintrc --fail-on=I pylint/__init__.py` (should get 10.00/10 rating)

## Common Tasks

### Running specific test categories:
- Functional tests: `pytest tests/test_functional.py -k "test_name" -v`
- Individual functional test: `pytest "tests/test_functional.py::test_functional[abstract_class_instantiated]" -v` (~1 second)
- Unit tests: `pytest tests/test_self.py -v`
- Quick smoke test: `pytest tests/test_func.py tests/test_check_parallel.py -v` (~2 seconds, 53 tests)

### Understanding the codebase structure:
```
pylint/                    # Main package
├── checkers/             # All pylint checkers (rules)
├── config/               # Configuration handling
├── message/              # Message system
├── reporters/            # Output formatters
├── testutils/            # Testing utilities
└── extensions/           # Optional extensions

tests/                     # Test suite
├── functional/           # Functional test files (.py files with expected output)
├── test_*.py            # Unit tests
└── data/                # Test data files

doc/                      # Documentation
├── user_guide/          # User documentation
├── development_guide/   # Developer documentation
└── additional_tools/    # Tools documentation
```

### Key files to know:
- `pyproject.toml` -- Main configuration (dependencies, build, tools)
- `tox.ini` -- Multi-environment testing configuration
- `.pre-commit-config.yaml` -- Code quality checks configuration
- `pylintrc` -- Pylint's own configuration
- `script/` -- Utility scripts for development

### Creating new checkers:
- Use `python script/get_unused_message_id_category.py` to get unused message IDs (outputs next available ID)
- Look at existing checkers in `pylint/checkers/` for patterns
- Add functional tests in `tests/functional/`

### Working with functional tests:
- Tests are in `tests/functional/` with `.py` files and corresponding `.txt` files for expected output
- Run individual functional test: `pytest tests/test_functional.py::test_functional[test_name] -v`

## Critical Timing Information

- **NEVER CANCEL:** All operations that show "NEVER CANCEL" may take significant time
- Functional test suite: 60 seconds (set timeout to 120+ seconds)
- Documentation build: 180 seconds (set timeout to 300+ seconds)
- Full pylint self-check: 20 seconds (set timeout to 60+ seconds)
- Individual test files: 1-15 seconds

## Known Issues and Workarounds

- **Network connectivity required:** Documentation build and pre-commit setup require internet access
- **Tox may fail:** In isolated environments, use direct pytest and pip commands instead of tox
- **Import errors in self-check:** Some import errors when running pylint on itself are expected (git dependencies not installed)

## Environment Limitations

- Some network-dependent operations may fail in isolated environments
- Use direct pip and pytest commands when tox environments fail to build
- Documentation build requires network access to fetch external inventories

Always build and exercise your changes by running pylint on sample code to ensure functionality works correctly.