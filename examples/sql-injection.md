# SQL injection: evidence before escalation

Authored reference review, not a captured agent run. The input is the original
smoke-test function. No caller, driver, schema, or deployment is supplied.

## Prompt

Use AI Engineering Reviewer in STANDARD mode. Evaluate correctness, security, and
maintainability. Do not modify files.

```javascript
function findUser(email) {
  return db.query(`SELECT * FROM users WHERE email = '${email}'`);
}
```

## Reference review

### Overall assessment

The function is concise, but directly interpolates a value into SQL. Fix that
construction before using it with untrusted input. The available snippet does not
establish the caller's authentication behavior or the database schema.

### Findings

**HIGH — unsafe SQL construction, `findUser`, line 2 of the snippet.**

Verified code-level defect: `email` becomes part of the SQL text. An apostrophe
can terminate the quoted value; for example, `x' OR '1'='1` changes the predicate.
Attacker control and reachability are unverified, so authentication bypass and
production exposure are not confirmed. HIGH reflects the consequence if untrusted
input reaches this boundary; CRITICAL requires more impact evidence.

Use the actual driver's parameter-binding API. Do not rely on manual escaping or
generic sanitization. For a promise-based PostgreSQL `pg` client, a minimal fix is:

```javascript
function findUser(email) {
  return db.query('SELECT * FROM users WHERE email = $1', [email]);
}
```

This intentionally preserves the existing return contract. The `pg` assumption
must be checked before applying it; other drivers use different APIs. Parameters
bind values, not table names or sort directions; dynamic identifiers need a fixed
allowlist or a supported identifier API.

**Open questions, not additional confirmed defects:**

- Does the caller need the raw result or a single user? Read the caller before changing it.
- Which columns are needed, and are any sensitive fields exposed? `SELECT *` alone does not prove a leak.
- What is the application's email identity policy, and how is uniqueness enforced? Do not add lowercasing without checking writes and schema.

### What is working well

The lookup has a single responsibility. Parameter binding is a targeted correction;
there is no demonstrated need for a repository framework or a rewrite.

### Priority fixes

1. Confirm the driver and parameterize the lookup.
2. Trace the entry point, caller, and schema to establish impact and contract.
3. Add a driver/database integration test: the payload is treated as one literal
   email and cannot return unrelated users. Cover apostrophes and unknown emails.

No tools or tests were run for this reference review. A mocked query assertion
alone would not prove how a real database parses the query.

### Engineering takeaway

Separate code from data at the query boundary. Separate what the snippet proves
from what the surrounding application might make exploitable.
