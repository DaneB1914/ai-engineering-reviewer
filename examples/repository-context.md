# Repository context can remove a finding

Authored reference review. The synthetic fixtures below are review inputs; they
are not a deployed application. See [the evaluation cases](../evals/cases.json).

## Prompt

Use AI Engineering Reviewer in STANDARD mode. Review `find-user.mjs` and inspect
its caller and schema before reporting defects. Do not modify files or run a database.

## Evidence

- [find-user.mjs](../evals/fixtures/repository-context/find-user.mjs) uses a `pg`
  value parameter and selects only `id` and `email`.
- [handler.mjs](../evals/fixtures/repository-context/handler.mjs) consumes the raw
  driver's `rows` property and returns 404 on an empty result.
- [schema.sql](../evals/fixtures/repository-context/schema.sql) enforces exact email
  uniqueness. Its comment states that matching is intentionally case-sensitive.

## Reference review

### Overall assessment

No material defect is demonstrated in the supplied lookup and caller. The query
and caller agree on the return shape. The schema supports the stated identity policy.

### Findings

No meaningful issues found in the supplied scope. `find-user.mjs:2` binds the email
as a value. `handler.mjs:3` destructures `rows`, and `handler.mjs:4` handles no match.
Returning the driver envelope is therefore not a broken contract here.

### What is working well

The query selects explicit fields. The unique constraint prevents duplicate exact
email identities. There is no evidence requiring lowercasing or an extra data layer.

### Priority fixes

None demonstrated. If this path is exposed publicly, inspect authentication and
authorization at its routing boundary next; those files were not supplied, so this
review cannot assess access control or call the endpoint production-ready.

### Engineering takeaway

A function name is weaker evidence than its actual contract. Trace the consumer
before normalizing a return value or changing identity semantics.

This reference review reasons from the supplied text. No database was started and
no integration tests were run.
