# AI Engineering Reviewer

[![Validate](https://github.com/DaneB1914/ai-engineering-reviewer/actions/workflows/validate.yml/badge.svg)](https://github.com/DaneB1914/ai-engineering-reviewer/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Engineering feedback with evidence, priorities, and reasons.**

An open-source Agent Skill for reviewing code, technical designs, and implementation
plans. It guides an assistant to trace relevant code paths, separate verified
defects from untested risks, recommend proportionate fixes, and teach the engineering
principles behind significant recommendations.

Designed for Codex, Claude Code, and Claude custom skills using the shared
[Agent Skills format](https://agentskills.io/specification). It is an instruction
workflow: results depend on the model, tools, permissions, and context available.

## A review should change your next decision

| Situation | Expected review behavior |
| --- | --- |
| User input interpolated into SQL | Identify the unsafe construction; recommend driver-specific parameters; state what is unknown about reachability. |
| A function returns a database result | Read its callers before declaring the return contract broken. |
| A small product has a large proposed architecture | Connect each component to a requirement; recommend the smallest design that meets it. |
| The implementation is sound | Say so. Do not invent findings to fill a quota. |

Repository access makes the review stronger: the skill asks the agent to read
project instructions, inspect callers, configuration and dependencies, trace
important paths, and cite exact file locations. Reviews preserve source files
unless changes are requested. Tests run only when permitted and appropriate.

## Install

Clone this repository into a separate checkout, inspect [SKILL.md](SKILL.md), and
copy the skill files into one of these locations. **Do not replace an existing
installation without comparing it first.** The repository root is the canonical
skill folder; development tooling and examples do not need to be installed.

| Host | Project installation | Personal installation |
| --- | --- | --- |
| Codex | `.agents/skills/ai-engineering-reviewer/` | `~/.agents/skills/ai-engineering-reviewer/` |
| Claude Code | `.claude/skills/ai-engineering-reviewer/` | `~/.claude/skills/ai-engineering-reviewer/` |
| Claude | Upload the generated ZIP in Customize > Skills and enable it | Managed in Claude |

Copy `SKILL.md` and `LICENSE`; optionally include `agents/openai.yaml` for Codex UI
metadata. On Windows, `~` means your user profile folder. Start a new agent session
if the skill does not appear. See the official [Codex guide](https://developers.openai.com/codex/skills),
[Claude Code guide](https://code.claude.com/docs/en/skills), and
[Claude upload guide](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
for host-specific discovery and availability.

To produce the minimal, portable ZIP locally, use Python 3.11 or later:

```sh
python -m pip install -r requirements-dev.txt
python scripts/package_skill.py
```

This writes `dist/ai-engineering-reviewer.zip`, containing one top-level
`ai-engineering-reviewer/` directory with the skill, license, and optional Codex
metadata. It never copies arbitrary files from the checkout. CI also builds this
ZIP as a workflow artifact; it does not automatically upload it to any agent.

## Use

Codex:

```text
$ai-engineering-reviewer Review the current changes in STANDARD mode.
Trace relevant callers, cite evidence, and distinguish defects from untested risks.
Do not modify files.
```

Claude Code:

```text
/ai-engineering-reviewer Review src/auth in SECURITY mode.
Check authorization boundaries and data exposure. Do not modify files.
```

Claude:

```text
Use my AI Engineering Reviewer skill in ARCHITECTURE mode.
Review the attached design for an early-stage app with a small team.
Identify justified complexity and recommend the smallest useful changes.
```

Provide the relevant code or accessible files. A repository link alone does not
grant access. When the host exposes tool activity, check that it read `SKILL.md`;
an assistant saying it used the skill is weaker evidence than an observed file read.
Do not request private reasoning as proof of activation.

## Review modes

| Mode | Use it for |
| --- | --- |
| QUICK | The most important issues only |
| STANDARD (default) | Balanced correctness, security, architecture, and maintainability |
| DEEP | Edge cases, failure modes, tests, and architecture tradeoffs |
| SECURITY | Vulnerabilities and trust boundaries |
| ARCHITECTURE | Design, complexity, scalability, and maintainability |

Reviews include an overall assessment, prioritized findings, sound decisions worth
retaining, priority fixes, and a short engineering takeaway. Significant findings
include location, evidence, impact, correction, and relevant tradeoffs. Severity
and confidence are separate: missing context must not become a confirmed exploit.

## See the judgment, not just the prompt

- [SQL injection](examples/sql-injection.md): unsafe JavaScript query, a calibrated review, and a `pg` correction.
- [Repository context](examples/repository-context.md): callers and schema prevent false-positive findings.
- [Architecture](examples/architecture.md): an early-stage design evaluated without defaulting to a rewrite.

These are authored reference examples, not captured model outputs or benchmark results.

## Validation and evaluation

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

CI runs the same checks on Linux and Windows. The validator checks skill metadata,
local Markdown file targets, YAML files, and the evaluation manifest. Tests exercise
invalid inputs, link containment, and deterministic packaging. External URLs and
Markdown anchor fragments are not checked. No model credentials are required.

[Behavioral evaluation](evals/README.md) covers injection, context-dependent findings,
architecture tradeoffs, clean code, and hostile instructions inside review material.
Run those cases in fresh agent sessions and record the model and observed evidence.
**Structural CI does not measure review quality or prove cross-host activation.**
No automated model benchmark or host installation test is claimed for this release.

## Boundaries

This skill is not a security certification, static analyzer, or autonomous review
service. It cannot guarantee defect detection or production readiness. Its review
constraints are instructions, not a permissions enforcement layer. Keep normal
agent controls in place, review suggested changes, and verify critical findings.

The skill does not need API keys, extra MCP servers, background services, or runtime
dependencies. Python and PyYAML are only for repository validation and packaging.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for changes and evaluation expectations,
[SECURITY.md](SECURITY.md) for vulnerability reporting, and
[CHANGELOG.md](CHANGELOG.md) for version history. Maintained by
[Dane Babcock](https://github.com/DaneB1914). Licensed under [MIT](LICENSE).
