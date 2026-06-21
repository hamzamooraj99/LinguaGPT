# Local Language Tutor Memory MCP

A minimal, local-first FastMCP server that stores language tutoring memory in
human-editable Markdown files. It is deliberately only a storage and retrieval
layer: the connected language model performs all teaching, correction, learner
evaluation, and curriculum decisions.

## Project layout

```text
server.py                 FastMCP server and validated storage operations
templates/                Default Markdown files used during initialization
tutor_data/<language>/    Local learner data (one directory per language)
TUTOR_INSTRUCTIONS.md     Instructions for the language-model tutor
tests/                    Standard-library verification tests
```

Each language directory contains the profile, plan, progress, vocabulary,
mistakes, scenarios, latest summary, active-session checkpoint, latest homework,
delivery drafts, permanent session logs, and lossless context archives.

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

## Setup and run

Python 3.10 or newer is recommended.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

The default transport is FastMCP's stdio transport. Configure your MCP client to
launch `python` with the absolute path to `server.py` as its argument.

## Tools

- `initialize_language_profile`: creates a complete profile. Existing files are
  preserved; pass `overwrite_existing=true` to replace only an existing profile
  and lesson plan with the supplied content.
- `read_language_context`: returns only the bounded active teaching context; it
  never loads permanent session logs, delivery drafts, or archives.
- `write_language_file`: replaces one explicitly whitelisted Markdown file,
  including homework and delivery drafts.
- `append_session_log`: creates a unique UTC-timestamped session file and updates
  `latest-summary.md`, then resets `active-session.md`.
- `save_session_checkpoint`: replaces the concise active-session state during a
  long lesson so the AI can recover after client-side context compaction.
- `get_language_context_status`: reports character counts and recommends
  compaction for cumulative files at 12,000 characters.
- `compact_language_file`: archives a complete cumulative file and replaces it
  with concise Markdown supplied by the AI.
- `list_language_file_archives` and `read_language_file_archive`: retrieve one
  validated historical context version on demand without loading all archives.
- `list_languages`: returns valid language directories alphabetically.

Language identifiers are normalized to lowercase and may contain letters, digits,
and hyphens only. Filenames are selected from a fixed whitelist; callers cannot
provide arbitrary paths. All text is read and written as UTF-8 beneath
`tutor_data/`.

## Context and retention model

`active-session.md`, `latest-summary.md`, `latest-homework.md`, and both delivery
drafts are bounded because they are replaced. Historical `sessions/` and
`archives/` grow linearly on disk but are not loaded into model context.

Profile, plan, progress, vocabulary, mistakes, and scenarios can accumulate over
time. The status tool flags any one of these at 12,000 characters and also warns
when total active context reaches 36,000 characters. These are character-based
heuristics, not exact model-token measurements. The AI then calls the compaction
tool with a concise replacement; the full original is retained in
`archives/<file-stem>/<UTC timestamp>.md`. Python never summarizes or decides what
learning content to retain.

Email and WhatsApp files are drafts only. This project performs no network calls
and does not send messages.

## Verify

```powershell
python -m unittest discover -s tests -v
```

The included `tutor_data/german/` directory is example data and can be edited or
removed. There is no database, network service, authentication layer, web UI, or
automatic backup. Files are local to the machine running the server.
