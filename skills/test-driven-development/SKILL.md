---
name: test-driven-development
description: Guides implementation with a verified red-green-refactor cycle and tests that assert caller-visible behavior. Use when a user requests TDD, test-first development, or a red-green-refactor approach for a feature or bug fix.
---

# Test-Driven Development

Use a small, repeatable test loop for one behavior at a time. Follow repository instructions for test placement, commands, approvals, and required checks.

## Start with a behavior

1. Identify the caller's entry point, the desired observable result, and one concrete example. For a bug, capture the reported symptom. Check nearby tests and the project's test command. Done when the expected result can be stated independently of the implementation.
2. Check the current baseline with the relevant existing tests. If unrelated failures exist, record them before adding a test. Done when the baseline is known.

## Red

3. Add one focused test through the caller's entry point. Assert a return value, state change, emitted output, persisted data, or documented error. Fake only external boundaries; run the matching, validation, and business logic for real. Use a concrete expected value, not one calculated by the code under test.
4. Run that test before changing production behavior. Confirm it fails for the missing behavior, not because of an import, fixture, or setup error. If it passes, strengthen the test or reassess whether the behavior is already implemented. Done when the intended failure is observed and recorded.

## Green

5. Make the smallest production change that satisfies the new test. Run the focused test again. Do not weaken, delete, or skip the test to obtain a pass. Done when the test passes and its assertion still checks the intended behavior.

## Refactor and verify

6. Improve names, structure, and duplication only after green. Rerun the focused test after each meaningful change. Done when the behavior stays green.
7. Run the relevant surrounding tests and required project checks. Inspect the diff for accidental scope changes. Report the red failure, the green result, the broader checks, and any remaining limitation. Done when the requested behavior is demonstrated through its real entry point.

If the code has no usable test seam, first protect existing behavior with a characterization test, then make the smallest structure change that enables a meaningful failing test. Resume the red-green-refactor loop from there.

Example: For a request that an unknown widget ID return HTTP 404, send the request through the HTTP route and assert the status and error body. A test that only checks whether a repository mock was called does not establish that client-visible behavior.
