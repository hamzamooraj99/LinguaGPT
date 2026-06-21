# AGENTS.md

## Purpose

This repository contains a local MCP-based language tutoring memory system.

The MCP server is responsible only for storage, retrieval, and management of learning data.

The language model is responsible for all teaching behavior.

Do not move teaching logic into Python unless explicitly requested.

---

## Development Philosophy

Prioritize:

1. Simplicity
2. Readability
3. Local-first design
4. Human-editable data
5. Minimal dependencies

Avoid:

- Databases
- Web frameworks
- Authentication systems
- Frontend applications
- Complex abstractions
- Premature optimization

Markdown files are the source of truth.

---

## Architecture Principles

The system consists of:

1. MCP tools
2. Local markdown storage
3. Tutor instruction files

The MCP server should behave like a filesystem-backed memory layer.

It should not:

- Generate lessons
- Evaluate language proficiency
- Create teaching strategies
- Make curriculum decisions

These responsibilities belong to the language model.

---

## Storage Rules

All user data must be stored under:

```txt
tutor_data/
```

Each language has its own directory.

Example:

```txt
tutor_data/
  german/
  italian/
  spanish/
```

All files must remain human-readable.

Use UTF-8 encoding.

Do not introduce databases.

---

## Implementation Rules

Prefer:

- pathlib
- dataclasses where useful
- type hints
- small functions

Avoid:

- global state
- unnecessary classes
- large inheritance hierarchies

Keep the codebase approachable for a single developer.

---

## MCP Tool Design

Each MCP tool should:

- perform one responsibility
- validate inputs
- return useful error messages
- fail safely

Do not create 'god tools' that perform multiple unrelated actions.

---

## Security

Prevent:

- path traversal
- arbitrary file writes
- writes outside tutor_data

Whitelist allowed files where appropriate.

Never trust user-provided paths.

---

## Testing

Before completing any task:

1. Verify the code runs.
2. Verify files are created correctly.
3. Verify invalid paths are rejected.
4. Verify UTF-8 content is preserved.

---

## Project Phases

Phase 1:
- Project structure
- Templates
- Initialization tools

Phase 2:
- Read/write tools
- Validation
- Error handling

Phase 3:
- Session logging
- Summaries
- Documentation

Do not implement future phases unless explicitly requested.

---

## When Unsure

Choose the simplest implementation that satisfies the requirement.

Favor boring solutions over clever solutions.
