# Live agent turn

## Claim

An agent using a selected production configuration can complete one bounded request through its model and required tool services. This check is opt-in when it incurs cost, accesses remote data, or writes external artifacts.

## Entry and proof

- Use the documented runner or a small driver that follows the same construction and invocation path for one request.
- Check credentials, service reachability, backing stores, and tracing settings relevant to that request. Identify the exact configuration used.
- Capture the request, selected capabilities, tool arguments and results, intermediate state or handles, final response, and retrievable artifacts relevant to the claim. Redact secrets and sensitive payloads.
- Record missing prerequisites as skipped with the remaining unproven claim. Treat a model answer as evidence for that run, not as a deterministic guarantee.

If the request can launch a costly or externally mutating job, establish its effects and stopping condition before running it. Assess what a failed attempt did before retrying.
