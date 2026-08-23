<p align="center">
  <img src="logo/logo_lrg.png" alt="LinguaMCP — the model teaches, LinguaMCP remembers" width="180">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/protocol-MCP-6D4AA8.svg" alt="MCP">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/tests-15%2F15-3E7D5A.svg" alt="15/15 tests">
  <img src="https://img.shields.io/badge/data-100%25%20local-3E7D5A.svg" alt="100% local">
  <img src="https://img.shields.io/badge/license-GPLv3-yellow.svg" alt="GPLv3 License">
</p>

<h3 align="center">Any model can teach a language. LinguaMCP makes sure it still knows your learner next week.</h3>

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Then point any MCP-compatible client at `python server.py`. No account, no database, no cloud — learner memory is Markdown files under `tutor_data/` that you own and can read.

> **The model teaches. LinguaMCP remembers.** It stores learner profiles, lesson plans, progress, vocabulary, mistakes, scenarios, homework, session checkpoints, and summaries as human-readable files on your machine — and does none of the tutoring itself.

---

## Wait — what *is* this?

Most language-learning chats lose continuity the moment you close the window. The model re-meets your learner every session: no memory of the last mistake, no running vocabulary, no plan for what comes next.

LinguaMCP is the memory layer that fixes that — a small, filesystem-backed MCP server that gives an AI tutor durable, human-readable state **without turning the server into a tutor.**

| LinguaMCP **is** | LinguaMCP is **not** |
|---|---|
| a local memory layer — every learner is a folder of Markdown you own | a cloud service, account, or subscription |
| filesystem-backed and human-readable — the files *are* the source of truth | an opaque database or vector store |
| a set of narrow, validated tools the model calls to read and write context | a "god tool" that does everything through one endpoint |
| deliberately model-led — Python never grades or generates lessons | a tutor, curriculum engine, or proficiency judge |

**Concretely, installing it gives you:** an MCP server exposing ten validated tools, one Markdown workspace per language under `tutor_data/`, an optional Windows desktop launcher, and an audit trail — with teaching, grading, and curriculum strategy left entirely to the connected model and the user.

---

## The loop

```
  MODEL ──→  initialize_language_profile
              │
              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  READ BOUNDED CONTEXT   read_language_context                 │
  │  active session + summary + profile — never the full          │
  │  archives. The model teaches from a small, current view.      │
  └──────────────────────────────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  TEACH  (the connected model — LinguaMCP stays out of it)     │
  │  lessons, corrections, homework, curriculum strategy:         │
  │  all model intelligence, none of it server-side logic.        │
  └──────────────────────────────────────────────────────────────┘
              │   approved writes only, whitelisted files
              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  PERSIST   write_language_file · save_session_checkpoint      │
  │  profile, progress, vocab, mistakes, homework, delivery       │
  │  drafts — each write validated, path-traversal rejected.      │
  └──────────────────────────────────────────────────────────────┘
              │
              ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  ARCHIVE & COMPACT   append_session_log · compact_language_   │
  │  file · get_language_context_status                           │
  │  permanent timestamped logs on disk; active context stays     │
  │  bounded; the status tool flags files for model-led compaction.│
  └──────────────────────────────────────────────────────────────┘
              │
              ▼
  next session:  read_language_context returns a small, current view —
                 full history archived, ready but out of the way.
```

---

## What it is responsible for

| It **does** | It **does not** |
|---|---|
| create learner profiles from templates | generate lessons |
| return bounded teaching context | grade the learner |
| write approved, whitelisted files | decide curriculum strategy |
| save active-session checkpoints | send emails or WhatsApp messages |
| append permanent session logs | run a web app or database |
| archive and report on compaction | judge proficiency |

Those right-hand responsibilities stay with the connected language model and the user. That separation is the whole design: Python moves bytes safely; the model does the thinking.

---

## Project layout

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

---

## Requirements

- Python 3.10 or newer
- An MCP-compatible client
- Local filesystem access to this repository

## Quick start

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

Configure your MCP client to launch `python` with the absolute path to `server.py` as its argument.

---

## Windows desktop launcher

LinguaMCP includes a small WPF desktop controller for starting and stopping the OAuth-enabled HTTP server without PowerShell, WSL, Docker, or a terminal window.

Run this once:

```bat
setup_launcher.cmd
```

The setup creates `.venv/`, installs the dependencies, publishes the launcher, and adds a branded `LinguaMCP MCP` shortcut to the current user's desktop. Open the shortcut to:

- start the FastMCP server in OAuth HTTP mode
- stop the running server and its child process
- see the current process state
- inspect recent server output

The launcher runs this command without opening a terminal window:

```powershell
python server.py --http --oauth --allow-writes
```

Before opening the launcher, define `LINGUAMCP_OAUTH_PASSWORD` as a Windows user environment variable. The launcher inherits it without storing the password in the repository. Closing the launcher stops the server.

---

## HTTP mode

For clients that connect to an MCP endpoint over HTTP:

```powershell
python server.py --http
```

The default endpoint is:

```text
http://127.0.0.1:8000/mcp
```

HTTP mode is **read-only by default.** To let the client update learner files, opt in explicitly:

```powershell
python server.py --http --allow-writes
```

To bind to another interface, for example from Docker or another local-network machine:

```powershell
python server.py --http --host 0.0.0.0 --port 8000
```

To use a different endpoint path:

```powershell
python server.py --http --path /lingua
```

<details>
<summary><b>Authentication</b> — bearer tokens and single-user OAuth for exposed endpoints</summary>

For public tunnels or non-local access, require a bearer token:

```powershell
$env:LINGUAMCP_AUTH_TOKEN = "replace-with-a-long-random-secret"
python server.py --http --allow-writes --require-auth
```

Clients must then send:

```text
Authorization: Bearer replace-with-a-long-random-secret
```

For ChatGPT custom connectors that require OAuth, enable the built-in single-user OAuth flow:

```powershell
$env:LINGUAMCP_OAUTH_PASSWORD = "replace-with-a-long-random-password"
python server.py --http --oauth --allow-writes
```

Use your public tunnel host with these paths:

```text
Server URL: https://<your-tunnel-host>/mcp
Auth URL:   https://<your-tunnel-host>/oauth/authorize
Token URL:  https://<your-tunnel-host>/oauth/token
```

Use any stable client ID, such as `linguamcp-chatgpt`. Leave the client secret blank if your client allows it. During approval, enter the value from `LINGUAMCP_OAUTH_PASSWORD`.

OAuth discovery metadata is exposed at:

```text
/.well-known/oauth-authorization-server
/.well-known/oauth-protected-resource
```

The OAuth flow is intentionally single-user and local-first. It does not depend on an external identity provider.

</details>

---

## MCP tools

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

Language identifiers are normalized to lowercase and may contain only letters, digits, and hyphens. Filenames come from a fixed whitelist. **Callers cannot write arbitrary paths.**

---

## Data model

LinguaMCP keeps active context small and recoverable:

- `active-session.md`, `latest-summary.md`, `latest-homework.md`, and delivery drafts are bounded because they are **replaced**, not appended.
- `sessions/` stores **permanent** timestamped lesson logs.
- `archives/` stores **full pre-compaction** versions of cumulative files.
- Profile, lesson plan, progress, vocabulary, mistakes, and scenarios can grow over time, so the status tool flags large files for model-led compaction.

Compaction is deliberately model-led: Python archives the original and writes the replacement supplied by the AI. It does not decide what learning content matters.

---

## Security posture

LinguaMCP is designed to be boring and local:

- all learner data stays under `tutor_data/`
- all text is read and written as UTF-8
- path traversal is rejected
- write targets are whitelisted
- HTTP writes require `--allow-writes`
- bearer-token auth is available for exposed HTTP endpoints
- tool calls are audited **without logging Markdown content**

Audit logs are written to:

```text
tutor_data/audit-log.jsonl
```

Use `--read-only` to block write-capable tools in any transport, and `--no-audit` to disable local JSONL audit logging.

---

## Verification

Run the test suite:

```powershell
python -m unittest discover -s tests -v
```

The tests verify initialization, safe writes, invalid path rejection, UTF-8 preservation, session logging, compaction archives, runtime security flags, and OAuth token handling.

---

## FAQ

**How is this different from just chatting with an AI tutor?**
A chat has no memory of your learner between sessions. LinguaMCP adds the state a chat can't hold: a durable profile, a running record of vocabulary and mistakes, permanent session logs, and a bounded context the model can re-read next time. The teaching is the easy part — continuity is what's missing.

**Does it teach or grade the learner?**
No. On purpose. Lesson generation, correction, curriculum strategy, and proficiency judgment all stay with the connected model. Python only reads and writes files safely. That boundary is enforced by the tool set, not by convention.

**Where does my data live?**
Under `tutor_data/`, one folder per language, as plain Markdown you can open, edit, diff, or delete. There is no database, no frontend, no external sender, and no automatic backup. Nothing leaves your machine unless you deliberately expose the HTTP endpoint.

**Can I expose it over the network?**
Yes — HTTP mode with `--allow-writes`, protected by a bearer token or the built-in single-user OAuth flow for clients like ChatGPT connectors. Writes are opt-in; read-only is the default.

**Won't the files grow forever?**
The status tool reports character counts and recommends compaction. When you agree, the model supplies a concise replacement and Python archives the full original under `archives/` — nothing is lost.

---

## Contributing and support

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a change and follow the [Code of Conduct](CODE_OF_CONDUCT.md).

Use [SUPPORT.md](SUPPORT.md) for support guidance. Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md).

## License

LinguaMCP is free software licensed under the [GNU General Public License v3.0](LICENSE).

---

<details>
<summary><b>Design principles</b></summary>

LinguaMCP favors:

- simple files over databases
- explicit tools over broad "god tools"
- local control over hosted state
- Markdown over opaque storage
- model intelligence over server-side teaching logic

The included `tutor_data/german/` directory is example data and can be edited or removed. There is no database, frontend, external sender, or automatic backup.

</details>

---

<sub>*A <b>lingua franca</b> is the shared tongue that lets strangers understand each other. LinguaMCP is the shared memory that lets a model and a learner pick up exactly where they left off.* · Built on FastMCP · GPLv3</sub>
