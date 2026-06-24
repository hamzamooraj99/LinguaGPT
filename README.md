<p align="center">
  <img src="logo/logo.png" alt="LinguaGPT logo" width="180">
</p>

# LinguaGPT

**Local-first language tutoring memory for AI tutors.**

LinguaGPT is a small MCP server that gives an AI language tutor durable,
human-readable memory without turning the server into a tutor. It stores learner
profiles, lesson plans, progress, vocabulary, mistakes, scenarios, homework,
session checkpoints, and summaries as Markdown files on your machine.

The model teaches. LinguaGPT remembers.

## Why LinguaGPT

Most language-learning chats lose continuity. LinguaGPT solves that by giving an
MCP-compatible client a clean local memory layer:

- **Local by default**: learner data lives under `tutor_data/`.
- **Human-readable**: Markdown files are the source of truth.
- **Model-led teaching**: no lesson generation or proficiency judgment in Python.
- **Safe file access**: tools validate language IDs and whitelist writable files.
- **Context-aware retention**: active context stays bounded while full history is
  archived on disk.
- **Minimal stack**: FastMCP, Python, Markdown, and the filesystem.

## What It Is

LinguaGPT is a filesystem-backed MCP memory server for language tutoring.

It is responsible for:

- creating language learner profiles
- reading bounded teaching context
- writing approved learner files
- saving active-session checkpoints
- appending permanent session logs
- archiving compacted long-running files
- reporting context size and compaction recommendations

It is not responsible for:

- generating lessons
- grading the learner
- deciding curriculum strategy
- sending emails or WhatsApp messages
- running a web app or database

Those responsibilities stay with the connected language model and the user.

## Project Layout

```text
server.py                 FastMCP server and validated storage operations
templates/                Default Markdown files used during initialization
tutor_data/<language>/    Local learner data, one directory per language
TUTOR_INSTRUCTIONS.md     Tutor-facing model instructions
tests/                    Standard-library verification tests
requirements.txt          Python dependencies
```

Each language gets its own Markdown workspace:

```text
tutor_data/<language>/
  00-profile.md
  01-lesson-plan.md
  02-progress.md
  03-vocabulary.md
  04-mistakes.md
  05-scenarios.md
  active-session.md
  latest-summary.md
  latest-homework.md
  delivery/
    latest-email.md
    latest-whatsapp.md
  sessions/
  archives/
```

## Requirements

- Python 3.10 or newer
- An MCP-compatible client
- Local filesystem access to this repository

## Quick Start

Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the server with the default stdio transport:

```powershell
python server.py
```

Configure your MCP client to launch `python` with the absolute path to
`server.py` as its argument.

## HTTP Mode

For clients that connect to an MCP endpoint over HTTP:

```powershell
python server.py --http
```

The default endpoint is:

```text
http://127.0.0.1:8000/mcp
```

HTTP mode is read-only by default. To let the client update learner files, opt in
explicitly:

```powershell
python server.py --http --allow-writes
```

To bind to another interface, for example from Docker or another local-network
machine:

```powershell
python server.py --http --host 0.0.0.0 --port 8000
```

To use a different endpoint path:

```powershell
python server.py --http --path /lingua
```

## Authentication

For public tunnels or non-local access, require a bearer token:

```powershell
$env:LINGUAGPT_AUTH_TOKEN = "replace-with-a-long-random-secret"
python server.py --http --allow-writes --require-auth
```

Clients must then send:

```text
Authorization: Bearer replace-with-a-long-random-secret
```

For ChatGPT custom connectors that require OAuth, enable the built-in single-user
OAuth flow:

```powershell
$env:LINGUAGPT_OAUTH_PASSWORD = "replace-with-a-long-random-password"
python server.py --http --oauth --allow-writes
```

Use your public tunnel host with these paths:

```text
Server URL: https://<your-tunnel-host>/mcp
Auth URL:   https://<your-tunnel-host>/oauth/authorize
Token URL:  https://<your-tunnel-host>/oauth/token
```

Use any stable client ID, such as `linguagpt-chatgpt`. Leave the client secret
blank if your client allows it. During approval, enter the value from
`LINGUAGPT_OAUTH_PASSWORD`.

OAuth discovery metadata is exposed at:

```text
/.well-known/oauth-authorization-server
/.well-known/oauth-protected-resource
```

The OAuth flow is intentionally single-user and local-first. It does not depend
on an external identity provider.

## MCP Tools

| Tool | Purpose |
| --- | --- |
| `initialize_language_profile` | Create a complete language profile from templates and supplied learner details. |
| `read_language_context` | Return bounded active teaching context without loading permanent logs or archives. |
| `write_language_file` | Replace one whitelisted Markdown file, including homework and delivery drafts. |
| `append_session_log` | Create a timestamped session log, update `latest-summary.md`, and reset `active-session.md`. |
| `save_session_checkpoint` | Replace the concise active-session state during a long lesson. |
| `get_language_context_status` | Report character counts and recommend compaction when files grow large. |
| `compact_language_file` | Archive a complete cumulative file and replace it with a concise model-supplied version. |
| `list_language_file_archives` | List validated historical archive versions for one file. |
| `read_language_file_archive` | Read one validated archive file on demand. |
| `list_languages` | Return available language directories alphabetically. |

Language identifiers are normalized to lowercase and may contain only letters,
digits, and hyphens. Filenames come from a fixed whitelist. Callers cannot write
arbitrary paths.

## Data Model

LinguaGPT keeps active context small and recoverable:

- `active-session.md`, `latest-summary.md`, `latest-homework.md`, and delivery
  drafts are bounded because they are replaced.
- `sessions/` stores permanent timestamped lesson logs.
- `archives/` stores full pre-compaction versions of cumulative files.
- Profile, lesson plan, progress, vocabulary, mistakes, and scenarios can grow
  over time, so the status tool flags large files for model-led compaction.

Compaction is deliberately model-led. Python archives the original and writes the
replacement supplied by the AI; it does not decide what learning content matters.

## Security Posture

LinguaGPT is designed to be boring and local:

- all learner data stays under `tutor_data/`
- all text is read and written as UTF-8
- path traversal is rejected
- write targets are whitelisted
- HTTP writes require `--allow-writes`
- bearer-token auth is available for exposed HTTP endpoints
- tool calls are audited without logging Markdown content

Audit logs are written to:

```text
tutor_data/audit-log.jsonl
```

Use `--read-only` to block write-capable tools in any transport and `--no-audit`
to disable local JSONL audit logging.

## Verification

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

The tests verify initialization, safe writes, invalid path rejection, UTF-8
preservation, session logging, compaction archives, runtime security flags, and
OAuth token handling.

## Design Principles

LinguaGPT favors:

- simple files over databases
- explicit tools over broad "god tools"
- local control over hosted state
- Markdown over opaque storage
- model intelligence over server-side teaching logic

The included `tutor_data/german/` directory is example data and can be edited or
removed. There is no database, frontend, external sender, or automatic backup.
