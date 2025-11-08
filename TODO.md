# TODO: dkjason Package Improvements

This document tracks improvements needed for the dkjason JSON serialization library.

**Last Updated:** 2025-11-08
**Total Issues:** 31 (7 High, 15 Medium, 9 Low)

---

## 🔴 HIGH PRIORITY (Critical - Fix Immediately)

### Security & Best Practices Issues

- [ ] **Fix potential XSS vulnerability in JSONP support** (`dkjason/jason.py:212-223`)
  - JSONP can be exploited for XSS attacks
  - Consider deprecating JSONP support or adding strict validation
  - Add Content-Security-Policy headers

- [ ] **Add input validation for callback parameter** (`dkjason/jason.py:198-199`)
  - Validate callback parameter against a whitelist pattern
  - Prevent injection attacks through callback manipulation

- [ ] **Fix encoding inconsistency** (`dkjason/jason.py:87,179`)
  - Replace 'u8' with 'utf-8' for clarity and standards compliance
  - Line 87: `return o.decode('u8')` → `return o.decode('utf-8')`
  - Line 179: `txt = txt.decode('u8')` → `txt = txt.decode('utf-8')`

- [ ] **Remove or update outdated pylint disable** (`dkjason/jason.py:5`)
  - Investigate if `# pylint:disable=E0202` is still needed
  - Update or remove based on current pylint version

- [ ] **Handle UnicodeEncodeError properly** (`dkjason/jason.py:137`)
  - Don't silently suppress the error with pragma: nocover
  - Either handle it properly or let it propagate

- [ ] **Add comprehensive error handling** (`dkjason/jason.py:152-162`)
  - obj_decoder assumes regex match succeeds without checking
  - Add proper error handling for malformed datetime strings

- [ ] **Update Python version requirements**
  - Drop Python 2 support officially
  - Update setup.py to require Python >= 3.8
  - Remove Python 2 compatibility code from tests

---

## 🟡 MEDIUM PRIORITY (Important - Fix Soon)

### Code Quality & Maintainability

- [ ] **Add type hints throughout the codebase**
  - Add type hints to all functions in jason.py
  - Use typing module for complex types
  - Consider using mypy for type checking

- [ ] **Add comprehensive docstrings**
  - Many functions lack proper docstrings
  - Follow Google or NumPy docstring style
  - Document parameters, return values, and exceptions

- [ ] **Clean up commented code** (`dkjason/jason.py:163-164`)
  - Remove commented datetime parsing code
  - If needed for reference, move to documentation

- [ ] **Improve test coverage to 100%**
  - Add test for numpy not installed case (line 92-94)
  - Remove or update Python 2 skip decorators in tests
  - Fix commented assertions in test_jsonp

- [ ] **Modernize packaging**
  - Add pyproject.toml with proper metadata
  - Use setuptools >= 64 with build backend
  - Add setup.cfg for configuration

- [ ] **Add GitHub Actions CI/CD**
  - Create workflow for running tests on push/PR
  - Test against multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
  - Add coverage reporting to codecov

- [ ] **Prepare for future Django upgrade**
  - Document Django 3.2 → 4.x migration requirements
  - Identify deprecated Django 3.2 features in use
  - Plan compatibility layer for smooth transition (2025)
  - Note: Currently targeting Django 3.2 LTS

- [ ] **Add pre-commit hooks**
  - Add isort for import sorting
  - Include flake8 or ruff for linting
  - Add mypy for type checking
  - Note: Not using black per project standards

### Performance Improvements

- [ ] **Optimize regex compilation** (`dkjason/jason.py:114-123`)
  - Move DATETIME_RE compilation to module level (already done)
  - Consider caching compiled patterns for other formats

- [ ] **Optimize _get_tag function** (`dkjason/jason.py:130-145`)
  - Redundant str() call on line 136
  - Simplify logic flow

- [ ] **Add caching for repeated serializations**
  - Consider LRU cache for frequently serialized objects
  - Profile to identify bottlenecks

### Documentation

- [ ] **Create comprehensive API documentation**
  - Use Sphinx for generating docs
  - Host on ReadTheDocs
  - Add usage examples and tutorials

- [ ] **Add CONTRIBUTING.md**
  - Guidelines for contributors
  - Code style guide
  - Testing requirements

- [ ] **Update README.rst**
  - Add more usage examples
  - Document all supported types
  - Add performance benchmarks

---

## 🟢 LOW PRIORITY (Nice to Have)

### Feature Enhancements

- [ ] **Add support for more types**
  - UUID serialization
  - Path objects (pathlib)
  - Enum support
  - dataclass support

- [ ] **Add configuration options**
  - Allow customizing datetime format
  - Configurable encoding for special types
  - Option to disable JSONP support

- [ ] **Add async support**
  - Async versions of dumps/loads
  - Support for async iterables

### Testing & Development

- [ ] **Add performance benchmarks**
  - Compare with standard json module
  - Benchmark against other serialization libraries
  - Add regression tests for performance

- [ ] **Add integration tests**
  - Test with real Django projects
  - Test with different database backends
  - Test with various ttcal configurations

- [ ] **Add property-based testing**
  - Use hypothesis for generating test cases
  - Ensure roundtrip consistency
  - Test edge cases automatically

### Code Organization

- [ ] **Split large module into smaller ones**
  - Separate encoder and decoder
  - Move Django-specific code to submodule
  - Create utils module for helpers

- [ ] **Add logging support**
  - Add debug logging for troubleshooting
  - Log warnings for deprecated features
  - Performance metrics logging

- [ ] **Add deprecation warnings**
  - Warn about JSONP usage
  - Deprecate old function names
  - Guide users to modern alternatives

---

## 📊 Issue Summary

| Priority | Count | Status |
|----------|-------|--------|
| High     | 7     | 🔴 Todo |
| Medium   | 15    | 🟡 Todo |
| Low      | 9     | 🟢 Todo |
| **Total**| **31**| **Todo** |

---

## 🎯 Next Actions

1. **Immediate**: Fix security vulnerabilities (JSONP validation)
2. **This Week**: Fix encoding issues and error handling
3. **This Month**: Add type hints and improve test coverage
4. **This Quarter**: Modernize packaging and add CI/CD