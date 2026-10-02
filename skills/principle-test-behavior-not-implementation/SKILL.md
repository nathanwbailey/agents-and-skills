---
name: principle-test-behavior-not-implementation
description: "Apply when writing, changing, or reviewing Python tests. Exercise the entry point a caller uses and assert a concrete result or observable effect. Rewrite tests that only inspect mocks, repeat implementation constants, or assert their own fixtures."
disable-model-invocation: true
---

# Test Behavior, Not Implementation

A Python test should call the entry point its caller uses and check a result or effect the caller can observe. Use a concrete input and an independently written expected value.

Before keeping a test, ask: if the subject returned `None` and made no observable change, would this test still pass? If so, it probably does not check the behavior it claims to check. This is a diagnostic, not a rule that every valid function must return a value: a function may legitimately return `None` while writing a file, changing state, or raising a documented exception.

Common weak tests:

- **No useful assertion:** the test only executes code, or checks `result is not None`, `isinstance(result, dict)`, or `len(result) > 0` when the actual values matter.
- **Mock interaction only:** `mock.assert_called_once()` checks wiring but not the returned data, written payload, or other caller-visible effect.
- **Self-referential expectation:** `assert parse(value) == parse(value)`, or the expected value is calculated by the same function under test.
- **Constant or prompt pin:** `assert LIMITS.max_tools == 8` or `assert "You are" in PROMPT` merely repeats an implementation choice instead of checking the behavior that uses it.
- **Fixture asserts fixture:** the assertion checks data constructed by the test or a fixture, without exercising the subject.

Prefer a test such as:

```python
def test_slugify():
    assert slugify("Hello, World!") == "hello-world"
```

For a function whose result is an effect, call it and inspect that effect. For example, write to `tmp_path` and assert the file's exact contents. When a mock represents a boundary the subject does not own, assert the meaningful payload sent across it and, where applicable, the subject's result. Test an absent result alongside a concrete present case when absence alone could pass without working behavior.

Keep tests of real invariants, such as a foreign key matching an existing row, and tests that intentionally check a public typing contract with a Python type checker. Avoid deleting a valid test merely because its observable result is `None`.