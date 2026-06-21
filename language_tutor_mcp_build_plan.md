# Project: Local Language Tutor Memory via MCP

## Goal

Build a minimal local MCP server that lets ChatGPT act as a structured language tutor using local Markdown files as persistent memory.

The system should support:

1. Creating a learner profile.
2. Creating and storing a lesson plan.
3. Reading the current plan/progress before each lesson.
4. Tracking progress, vocabulary, mistakes, and session summaries.
5. Supporting scenario-based roleplay practice.
6. Keeping everything local, editable, and human-readable.

Do not build a web app. Do not use a real database. Use Markdown files and a small MCP server.

---

## Tech Stack

Use:

- Python
- FastMCP
- Markdown files for storage
- Local filesystem only

Recommended structure:

```txt
language-tutor-mcp/
  server.py
  tutor_data/
    german/
      00-profile.md
      01-lesson-plan.md
      02-progress.md
      03-vocabulary.md
      04-mistakes.md
      05-scenarios.md
      latest-summary.md
      sessions/
```

---

## Core MCP Tools

Implement these tools:

### 1. initialize_language_profile

Creates the folder/files for a target language.

Inputs:

```json
{
  "language": "german",
  "profile_markdown": "...",
  "lesson_plan_markdown": "..."
}
```

Behavior:

- Create tutor_data/{language}/
- Create all required markdown files if missing
- Save profile and lesson plan
- Initialize blank progress, vocabulary, mistakes, scenarios, latest-summary
- Create sessions/ folder

### 2. read_language_context

Reads all current tutor files for a language.

Returns:

- profile
- lesson plan
- progress
- vocabulary
- mistakes
- scenarios
- latest summary

### 3. write_language_file

Updates a specific file.

Allowed filenames:

- 00-profile.md
- 01-lesson-plan.md
- 02-progress.md
- 03-vocabulary.md
- 04-mistakes.md
- 05-scenarios.md
- latest-summary.md

### 4. append_session_log

Creates a dated session file and updates latest-summary.md.

### 5. list_languages

Returns available language folders.

---

## Tutor Behavior

At the start of every lesson:

- Read profile
- Read lesson plan
- Read progress
- Read vocabulary
- Read mistakes
- Read scenarios

At the end of every lesson:

- Update progress
- Update vocabulary
- Update mistakes
- Save session summary
- Create homework

Use guided correction before giving answers directly.

---

## Safety Requirements

- Prevent path traversal
- UTF-8 only
- Type hints
- Helpful errors
- Create folders automatically
- Do not overwrite existing data without permission

---

## Deliverables

1. server.py
2. requirements.txt
3. README.md
4. TUTOR_INSTRUCTIONS.md
5. Markdown templates
6. Example German profile

The MCP server should only manage memory and files.

The language model is responsible for all teaching behavior.
