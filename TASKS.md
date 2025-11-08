# TASKS: dkjason Development Tasks

This document outlines concrete development tasks organized by work sessions.

**Last Updated:** 2025-11-08
**Python Environments:**
- Virtualenv: `c:\srv\venv\dkjason311\Scripts\python.exe` (Python 3.11)
- WSL Python: `wsl python` (Python 3.10.12)

---

## 🚀 Quick Start Tasks (Session 1: ~2 hours)

### Task 1: Fix Critical Issues
```bash
# 1. Fix encoding issues
# Edit dkjason/jason.py:
#   Line 87: o.decode('u8') → o.decode('utf-8')
#   Line 179: txt.decode('u8') → txt.decode('utf-8')

# 2. Run tests to verify
DJANGO_SETTINGS_MODULE= c:/srv/venv/dkjason311/Scripts/pytest -v tests

# 3. Update test for encoding
# Add test in tests/test_jason.py:
# def test_utf8_encoding():
#     assert jason.dumps(b'hello') == '"hello"'
#     assert jason.loads(b'{"test": "value"}') == {"test": "value"}
```

### Task 2: Add Input Validation
```python
# Add to dkjason/jason.py (before line 212):
import re

CALLBACK_PATTERN = re.compile(r'^[a-zA-Z_$][a-zA-Z0-9_$]*$')

def validate_callback(callback):
    """Validate JSONP callback parameter for security."""
    if not callback:
        return False
    if not CALLBACK_PATTERN.match(callback):
        raise ValueError(f"Invalid callback name: {callback}")
    return True

# Update jsonp function:
def jsonp(callback, val, **kw):
    """Serialization with json callback."""
    if not validate_callback(callback):
        raise ValueError(f"Invalid callback parameter: {callback}")
    # ... rest of function
```

### Task 3: Improve Error Handling
```python
# Update obj_decoder in jason.py:
def obj_decoder(pairs):
    """Reverses values created by DkJSONEncoder."""
    # ... existing code ...
    if tag and tag == '@datetime:':
        val = str(val)
        m = DATETIME_RE.match(val)
        if not m:
            raise ValueError(f"Invalid datetime format: {val}")
        g = m.groupdict()
        # ... rest of function
```

---

## 📦 Modernization Tasks (Session 2: ~3 hours)

### Task 4: Add Type Hints
```python
# Create dkjason/py.typed file (marks package as typed)
touch dkjason/py.typed

# Update jason.py with type hints:
from typing import Any, Dict, Optional, Union, Type
import json

def dumps(val: Any,
          indent: Optional[int] = 4,
          sort_keys: bool = True,
          cls: Type[json.JSONEncoder] = DkJSONEncoder) -> str:
    """Dump json value, using our special encoder class."""
    return json.dumps(val, indent=indent, sort_keys=sort_keys, cls=cls)
```

### Task 5: Create pyproject.toml
```toml
# Create pyproject.toml:
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "dkjason"
version = "3.0.6"
description = "Helper module to send json encoded data from Python"
readme = "README.rst"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Datakortet"},
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries",
]
dependencies = [
    "Django>=3.2,<4.0",  # Staying on 3.2 LTS for now
    "ttcal>=1.0.5",
]

[project.optional-dependencies]
numpy = ["numpy>=1.20"]
test = [
    "pytest>=6.0",
    "pytest-cov>=2.12.1",
    "pytest-django>=4.0",
]
dev = [
    "isort",
    "mypy",
    "ruff",
    "pre-commit",
    # Note: Not using black per project standards
]

[tool.setuptools]
packages = ["dkjason"]

[tool.isort]
profile = "django"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
```

### Task 6: Add GitHub Actions CI
```yaml
# Create .github/workflows/ci.yml:
name: CI

on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]
        # Currently targeting Django 3.2 LTS
        # Will expand to 4.x/5.x in 2025
        django-version: ["3.2"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install Django~=${{ matrix.django-version }}.0
        pip install -e .[test]

    - name: Run tests
      run: |
        pytest -v --cov=dkjason --cov-report=xml tests/

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

---

## 🧪 Testing Tasks (Session 3: ~2 hours)

### Task 7: Improve Test Coverage
```python
# Add to tests/test_jason.py:

def test_numpy_not_installed(monkeypatch):
    """Test behavior when numpy is not installed."""
    monkeypatch.setattr('dkjason.jason.NUMPY', False)
    # Test that numpy.int64 handling is skipped

def test_encoding_consistency():
    """Test UTF-8 encoding consistency."""
    test_strings = [
        'hello',
        'héllo',
        '你好',
        '🎉',
    ]
    for s in test_strings:
        encoded = s.encode('utf-8')
        assert jason.dumps(encoded) == f'"{s}"'

def test_malformed_datetime():
    """Test handling of malformed datetime strings."""
    import pytest
    malformed = '{"k":"@datetime:not-a-date"}'
    with pytest.raises(ValueError):
        jason.loads(malformed)

def test_callback_validation():
    """Test JSONP callback validation."""
    import pytest
    # Valid callbacks
    assert jason.validate_callback('callback')
    assert jason.validate_callback('_callback')
    assert jason.validate_callback('$callback')

    # Invalid callbacks
    with pytest.raises(ValueError):
        jason.validate_callback('alert(1)')
    with pytest.raises(ValueError):
        jason.validate_callback('callback;alert(1)')
```

### Task 8: Add Pre-commit Configuration
```yaml
# Create .pre-commit-config.yaml:
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  # Note: Not using black per project standards

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff

# Install pre-commit:
# pip install pre-commit
# pre-commit install
```

---

## 📚 Documentation Tasks (Session 4: ~3 hours)

### Task 9: Create Comprehensive Documentation
```bash
# Create docs structure:
mkdir docs
cd docs

# Create docs/conf.py for Sphinx
# Create docs/index.rst
# Create docs/api.rst
# Create docs/examples.rst
# Create docs/changelog.rst

# Build documentation:
sphinx-build -b html docs docs/_build
```

### Task 10: Add Usage Examples
```python
# Create examples/basic_usage.py:
"""Basic usage examples for dkjason."""

from datetime import datetime, date
from decimal import Decimal
from dkjason import jason

# Basic types
data = {
    'string': 'hello',
    'number': 42,
    'decimal': Decimal('3.14'),
    'datetime': datetime.now(),
    'date': date.today(),
    'list': [1, 2, 3],
    'set': {1, 2, 3},
}

# Serialize
json_str = jason.dumps(data)
print(json_str)

# Deserialize
restored = jason.loads(json_str)
print(restored)

# Django integration
from django.http import HttpRequest
from dkjason.jason import response

def api_view(request):
    data = {'status': 'success', 'timestamp': datetime.now()}
    return response(request, data)
```

---

## 🔄 Continuous Improvement Tasks

### Task 11: Performance Benchmarks
```python
# Create benchmarks/performance.py:
import timeit
import json
from dkjason import jason

def benchmark_dumps():
    data = {
        'numbers': list(range(1000)),
        'strings': ['test' * 100 for _ in range(100)],
    }

    # Standard json
    std_time = timeit.timeit(
        lambda: json.dumps(data),
        number=1000
    )

    # dkjason
    dk_time = timeit.timeit(
        lambda: jason.dumps(data),
        number=1000
    )

    print(f"Standard json: {std_time:.3f}s")
    print(f"dkjason: {dk_time:.3f}s")
    print(f"Ratio: {dk_time/std_time:.2f}x")

if __name__ == '__main__':
    benchmark_dumps()
```

### Task 12: Security Audit
```bash
# Install security tools:
pip install bandit safety

# Run security scan:
bandit -r dkjason/
safety check

# Check for known vulnerabilities:
pip-audit
```

---

## 📋 Task Checklist

- [ ] Session 1: Critical Fixes (2 hours)
  - [ ] Fix encoding issues
  - [ ] Add input validation
  - [ ] Improve error handling

- [ ] Session 2: Modernization (3 hours)
  - [ ] Add type hints
  - [ ] Create pyproject.toml
  - [ ] Setup GitHub Actions CI

- [ ] Session 3: Testing (2 hours)
  - [ ] Improve test coverage to 100%
  - [ ] Add pre-commit hooks
  - [ ] Add integration tests

- [ ] Session 4: Documentation (3 hours)
  - [ ] Create Sphinx documentation
  - [ ] Add usage examples
  - [ ] Create API reference

- [ ] Ongoing: Maintenance
  - [ ] Performance benchmarks
  - [ ] Security audits
  - [ ] Dependency updates