# Pylint Development Instructions

Always follow these instructions first and fallback to additional search and context
gathering only if the information in these instructions is incomplete or found to be in
error.

## Issue Label Guidelines

Before attempting to fix any issue, check the GitHub issue labels using the GitHub API:

- If an issue is labeled with "Astroid", "Needs astroid update", "Needs astroid
  constraint", or "Needs astroid Brain 🧠", **ONLY** create regression tests
- Do **NOT** attempt to fix astroid-related issues as you cannot modify astroid from
  this repository
- For astroid-related issues, focus on creating comprehensive regression tests that
  reproduce the problem
- All other issues can be fixed normally following the standard development workflow

## Development Environment Setup

### Basic Installation

Clone and set up pylint development environment:

- `git clone https://github.com/pylint-dev/pylint` -- clone repository
- `cd pylint` -- enter directory
- `python3 -m venv venv` -- create virtual environment
- `source venv/bin/activate` -- activate virtual environment (Linux/Mac)
- `pip install -r requirements_test_min.txt` -- install test dependencies (~30 seconds)
- `pip install -e .` -- install pylint in editable mode (~30-60 seconds)

### Optional Setup Steps

- `pre-commit install` -- enable pre-commit hooks for autoformatting
- `pip install pre-commit` -- install pre-commit separately if needed

### Astroid Development (if needed)

If working on astroid changes:

- `git clone https://github.com/pylint-dev/astroid.git` -- clone astroid
- `pip install -e astroid/` -- install astroid in editable mode
- `cd astroid/ && git switch my-astroid-dev-branch` -- switch to development branch

## Running Tests

### Core Test Commands

- `pytest tests/test_functional.py -k test_functional` -- run functional tests (~60
  seconds, NEVER CANCEL, set timeout to 120+ seconds)
- `pytest tests/` -- run all tests (several minutes, NEVER CANCEL, set timeout to 300+
  seconds)
- `python3 -m pytest` -- run tests with local python
- `pytest tests/test_check_parallel.py -v` -- quick test file (~2 seconds)

### Specific Test Types

- **Functional tests:**
  `pytest "tests/test_functional.py::test_functional[missing_kwoa_py3]"` -- single
  functional test (~1 second)
- **Unit tests:** Located in `/tests/` directory, test specific pylint functionality
- **Configuration tests:** In `/tests/config/functional/` for testing configuration
  loading
- **Primer tests:** `pytest -m primer_stdlib --primer-stdlib` -- test on stdlib for
  crashes

### Test with Coverage

- `pytest tests/message/ --cov=pylint.message` -- run with coverage
- `coverage html` -- generate HTML coverage report

### Tox Usage (Optional)

- `python -m tox` -- run all tox environments
- `python -m tox -epy313` -- run Python 3.13 suite only
- `python -m tox -epylint` -- run pylint on pylint's codebase
- `python -m tox -eformatting` -- run formatting checks
- `python -m tox --recreate` -- recreate environments (recommended)
- `python -m tox -e py310 -- -k test_functional` -- run specific tests in tox

## Documentation

### Building Documentation

- `make -C doc/ install-dependencies` -- install doc dependencies (~10 seconds)
- `make -C doc/ html` -- build documentation (~3 minutes, NEVER CANCEL, set timeout to
  300+ seconds)
- `make -C doc/ clean` -- clean build files when starting from scratch
- `tox -e docs` -- alternative way to build docs

**Network dependency:** Documentation build requires internet access to fetch external
inventories.

## Validation and Quality Checks

### Running Pylint on Code

- `pylint --help` -- verify pylint installation works
- `pylint --disable=all --enable=E,F pylint/` -- run pylint on itself for errors only
  (~20 seconds)
- `pylint --rcfile=pylintrc --fail-on=I path/to/your/changes.py` -- standard pylint run
- `pylint --disable=all --enable=E,F,W path/to/your/changes.py` -- focus on errors and
  warnings

### Pre-commit and Formatting

- `pre-commit run --all-files` -- run all formatting checks (requires network for
  initial setup)
- **Network dependency:** pre-commit may fail in isolated environments due to hook
  downloads

### Validation Test Scenarios

Always test your changes with these validation scenarios:

- `echo "def badFunction(): pass" > /tmp/test_sample.py && pylint --enable=C0103 /tmp/test_sample.py`
  -- should find naming issues
- `pylint --help` and `pylint --list-msgs | head -10` -- verify CLI functionality
- `pylint --help-msg=C0103` -- should show invalid-name help
- `pylint --rcfile=pylintrc --fail-on=I pylint/__init__.py` -- should get 10.00/10
  rating

## Writing Tests

### Functional Tests

Located in `/tests/functional/`, consists of `.py` test files with corresponding `.txt`
expected output files:

- Annotate lines where messages are expected:
  `a, b, c = 1 # [unbalanced-tuple-unpacking]`
- Multiple messages on same line:
  `a, b, c = 1.test # [unbalanced-tuple-unpacking, no-member]`
- Use offset syntax for special cases: `# +1: [singleton-comparison]`
- **Run and update:**
  `python tests/test_functional.py --update-functional-output -k "test_functional[test_name]"`

### Test File Organization

- **New checkers:** Create `new_checker_message.py` in `/tests/functional/n/`
- **Extensions:** Place in `/tests/functional/ext/extension_name/`
- **Regression tests:** Place in `/tests/r/regression/` with `regression_` prefix
- **Configuration tests:** Place in `/tests/config/functional/`

### Configuration Test Files

Create `.result.json` files with configuration differences from standard config:

```json
{
  "functional_append": {
    "disable": [["a-message-to-be-added"]]
  },
  "jobs": 10
}
```

## Codebase Structure

```
pylint/                    # Main package
├── checkers/             # All pylint checkers (rules implementation)
├── config/               # Configuration handling and parsing
├── message/              # Message system and formatting
├── reporters/            # Output formatters (text, json, etc.)
├── testutils/            # Testing utilities and helpers
└── extensions/           # Optional extensions and plugins

tests/                     # Test suite
├── functional/           # Functional test files (.py + .txt expected output)
├── config/functional/    # Configuration functional tests
├── r/regression/         # Regression tests
├── test_*.py            # Unit tests
└── regrtest_data/       # Test data files

doc/                      # Documentation
├── user_guide/          # User documentation
├── development_guide/   # Developer and contributor documentation
│   ├── contributor_guide/    # Setup, testing, contribution guidelines
│   ├── technical_reference/  # Technical implementation details
│   └── how_tos/             # Guides for custom checkers, plugins
└── additional_tools/    # Tools documentation

script/                   # Development utility scripts
```

### Key Files

- `pyproject.toml` -- Main configuration (dependencies, build, tools)
- `tox.ini` -- Multi-environment testing configuration
- `.pre-commit-config.yaml` -- Code quality checks configuration
- `pylintrc` -- Pylint's own configuration
- `requirements_test_min.txt` -- Minimal test dependencies
- `.gitignore` do not add the 'venv' inside the .gitignore, don't commit the venv in the
  first place (humans add it to their global gitignore)

## Creating New Checkers

### Getting Started

- `python script/get_unused_message_id_category.py` -- get next available message ID
- Study existing checkers in `pylint/checkers/` for patterns
- Read technical reference documentation in `doc/development_guide/technical_reference/`
- Use `astroid.extract_node` for AST manipulation

### Workflow

1. Create checker class in appropriate `pylint/checkers/` file
2. Add functional tests in `tests/functional/`
3. Search existing code for warning message to find where logic exists
4. Test with sample code to ensure functionality works

## Pull Request Guidelines

### Before Submitting

- Use Python 3.8+ for development (required for latest AST parser and pre-commit hooks)
- Write comprehensive commit messages relating to tracker issues
- Keep changes small and separate consensual from opinionated changes
- Add news fragment: `towncrier create <IssueNumber>.<type>`
- Always launch `pre-commit run -a` before committing

### Documentation Changes

- Document non-trivial changes
- Generate docs with `tox -e docs`
- Maintainers may label issues `skip-news` if no changelog needed

### Contribution Credits

- Add emails/names to `script/.contributors_aliases.json` if using multiple identities

## Critical Timing Information

- **NEVER CANCEL:** All operations that show "NEVER CANCEL" may take significant time
- **Full test suite:** 60+ seconds (set timeout to 120+ seconds)
- **Documentation build:** 180 seconds (set timeout to 300+ seconds)
- **Functional tests:** 60 seconds (set timeout to 120+ seconds)
- **Pylint self-check:** 20 seconds (set timeout to 60+ seconds)
- **Individual test files:** 1-15 seconds
- **Installation steps:** 30-60 seconds each

## Environment Limitations and Workarounds

- **Network connectivity required:** Documentation build and pre-commit setup require
  internet access
- **Tox failures:** In isolated environments, use direct pytest and pip commands instead
  of tox
- **Import errors in self-check:** Some import errors when running pylint on itself are
  expected (git dependencies not installed)
- **Build environments:** Use direct pip/pytest commands when tox environments fail to
  build

Always validate your changes by running pylint on sample code to ensure functionality
works correctly.
