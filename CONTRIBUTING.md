# Contributing

Keep the skill focused on engineering judgment: evidence, calibrated impact,
proportionate corrections, and useful teaching. Small, demonstrated improvements
are easier to assess than a longer universal checklist.

1. Open an issue describing an observable failure or improvement. Use synthetic,
   minimal examples; remove credentials, private code, and identifying user data.
2. Make a focused change. `SKILL.md` is the single source of agent instructions;
   installation copies and ZIP files are generated, not maintained separately.
3. Install `requirements-dev.txt`, then run the three commands in the README's
   validation section. Add regression tests for changes to validation or packaging.
4. For instruction changes, run the relevant cases in [evals](evals/README.md) in a
   fresh session. Report host/model/version, date, whether the skill read was
   observed, case results, and limitations. Include redacted outputs when useful.
5. Explain what changed, why, and what you actually verified in the pull request.

Do not tune the skill to exact sample wording, add a required tool without a clear
need, or publish passing model scores based only on structural tests. Negative
results and honest uncertainty are useful contributions.

Changes are submitted under the repository's [MIT license](LICENSE). Be respectful,
specific, and constructive in technical discussions.
