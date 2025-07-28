# 0x03 ‑ Unittests & Integration Tests

> **ALX‑Backend‑Python module** – July 2025  
> Focus: writing clean, parameterized unit tests, using mocks, and building basic integration tests for third‑party APIs.

---

## 📚 Project Overview
| File | Purpose |
|------|---------|
| **`utils.py`**   | Helper functions you’d find in any backend project: nested‑dict traversal, JSON fetcher, and a memoization decorator. |
| **`client.py`**  | A tiny GitHub “org client” that consumes GitHub’s REST API. |
| **`fixtures.py`**| Static sample payloads used in integration tests (no live network calls). |
| **`test_utils.py`**   | Unit tests for every public helper in `utils.py`. |
| **`test_client.py`**  | Unit **and** integration tests for `GithubOrgClient`. |

---

## 📝 Learning Objectives
1. **Unit vs Integration tests** – know the boundary.
2. **`unittest` essentials** – `TestCase`, assertions, fixtures.
3. **Parameterization** with the `parameterized` package.
4. **Mocking & Patching** – replace `requests.get`, mock properties, count calls.
5. **Memoization** – testing cache behavior.
6. Organising tests so they run with  
   ```bash
   python -m unittest discover
