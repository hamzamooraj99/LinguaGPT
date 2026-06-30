# Security Policy

## Supported versions

Security fixes are applied to the latest version on the default branch. Older
commits and unofficial distributions are not supported.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue, discussion, or
pull request. Report them privately through GitHub's **Report a vulnerability**
feature in the Security tab of this repository.

Include the affected version or commit, reproduction steps, expected impact,
and any suggested mitigation. Remove learner data, credentials, tokens, and
other personal information from the report.

You should receive an acknowledgement within seven days. After validation, the
maintainer will coordinate remediation and disclosure. Please allow a
reasonable period for a fix before publishing details.

## Security scope

Reports are especially useful when they concern:

- path traversal or writes outside `tutor_data/`
- authentication or OAuth bypasses
- exposure of learner content, tokens, passwords, or audit data
- unsafe default network access
- dependency vulnerabilities that are exploitable in LinguaGPT

LinguaGPT is local-first software. Users remain responsible for securing their
host, MCP client, public tunnel, credentials, and backups.
