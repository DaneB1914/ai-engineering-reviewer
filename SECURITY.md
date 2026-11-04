# Security

The initial 0.1.x series is the currently maintained line. No response-time or
long-term support commitment is promised.

For vulnerabilities in this repository, use GitHub's private **Report a
vulnerability** option in the Security tab if it is available. Otherwise, open a
minimal issue asking the maintainer for a private reporting channel. Do not post
secrets, private source code, or an actionable disclosure of an unfixed issue.

For ordinary documentation problems, false-positive examples, or feature requests,
use an issue with a sanitized reproduction.

Reviews of another project's vulnerabilities belong with that project's maintainer,
not in this repository. The intentionally vulnerable snippet in
[the SQL example](examples/sql-injection.md) is teaching material and is not executed
by the skill or CI.

Treat repositories under review as untrusted input. Test commands can execute
arbitrary project code; inspect unfamiliar commands and isolate execution. The
skill's instructions do not replace host permissions or human review.
