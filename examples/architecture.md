# Architecture: spend complexity where requirements justify it

Authored reference review of a fictional early-stage product.

## Prompt and constraints

Use AI Engineering Reviewer in ARCHITECTURE mode. A two-person team is building a
private beta for about 100 invited users. It needs sign-in, image uploads, CRUD,
and occasional background image processing. No measured scaling problem or hard
availability target has been established. Review the proposal in
[architecture.md](../evals/fixtures/architecture.md).

## Reference review

### Overall assessment

The proposed services are plausible tools, but the design spends substantial
operational effort before establishing the need for independent services. Start
with one application, managed authentication/database/storage, and a bounded
background worker. Revisit boundaries when workload or team evidence supports them.

### Findings

**MEDIUM — untested delivery/maintenance risk, service topology.** The proposal
requires Kubernetes, Kafka, Redis, and five independently deployed services for a
small beta. There is no supplied workload evidence showing a need for those
boundaries. The likely cost is deployment, debugging, and failure recovery work
for two people. This is a design tradeoff, not a confirmed runtime defect.

Keep application modules separate inside one deployable. Add a queue or job table
when processing needs retries and background execution. Define job ownership,
retry limits, idempotency, and failure visibility before selecting infrastructure.

Independent services may be justified by measured workload isolation, regulatory
boundaries, separate owners, or independent release requirements. None is given.

**HIGH — untested access-control risk, direct client data/storage access.** The
proposal does not specify per-user data or object access policy. That omission
does not prove deployed data is exposed. Before launch, define ownership, enforce
authorization in the server or managed access policies, and test that one user
cannot read or modify another user's records or private images.

### What is working well

Managed authentication and object storage reduce implementation work. Background
processing is a useful boundary when image work can outlast an interactive request.

### Priority fixes

1. Define and test per-user access rules.
2. Reduce deployables and record the conditions that would justify splitting them.
3. Specify job retries, duplicate handling, and failure reporting.
4. Measure request latency, queue age, and costs before adding scaling components.

### Engineering takeaway

Complexity earns its place by satisfying a requirement. Managed services can reduce
operations work, but still need explicit authorization and failure semantics.

No infrastructure was inspected, deployed, or load-tested for this reference.
