# Packaging and Data Root Plan

## Goal

Make LinguaMCP easier to install and run by packaging it as a Python package with a console command, while moving learner data out of the installed code directory and into a user-controlled data folder.

## Recommended Distribution

Start with a pip package:

```powershell
pip install linguamcp
linguamcp
```

This fits the current architecture because LinguaMCP is a Python MCP server with Python dependencies and a CLI-style entrypoint.

Do not prioritize npm initially. An npm package would mostly be a wrapper around Python, which adds installation and support complexity without much benefit unless users specifically ask for `npx linguamcp`.

## Data Root Design

Runtime learner data should not be stored relative to the installed package directory. Installed package locations may be read-only, virtualenv-specific, shared, or replaced during upgrades.

Use this precedence order:

1. Explicit CLI flag:

   ```powershell
   linguamcp --data-root "D:\LinguaMCP\tutor_data"
   ```

2. Environment variable:

   ```powershell
   $env:LINGUAMCP_DATA_ROOT = "D:\LinguaMCP\tutor_data"
   linguamcp
   ```

3. Default visible user folder.

   On Windows, prefer:

   ```text
   C:\Users\<user>\LinguaMCP\tutor_data
   ```

   This is preferable to hiding data under `AppData` because LinguaMCP's value proposition is local, human-readable Markdown that users can inspect, edit, back up, and delete.

Avoid defaulting to `Documents` unless users choose it, because Windows `Documents` is often redirected to OneDrive and may unexpectedly sync private learner data.

## Phase 1: Core Server and Packaging

1. Add configurable data root support.
   - Add `--data-root` to the server CLI.
   - Add `LINGUAMCP_DATA_ROOT` as an environment fallback.
   - Default to `~/LinguaMCP/tutor_data`.
   - Keep tests able to pass temporary `data_root` values.

2. Stop relying on package-relative `tutor_data/`.
   - Keep templates package-relative.
   - Store runtime learner data, sessions, archives, and audit logs under the configured data root.
   - Default audit log to `<data-root>/audit-log.jsonl`.

3. Prepare Python packaging.
   - Move server code into a real package, for example `linguamcp/server.py`.
   - Add `pyproject.toml`.
   - Add a console script named `linguamcp`.
   - Include `templates/` as package data.

4. Update documentation.
   - Document the primary install path:

     ```powershell
     pip install linguamcp
     linguamcp
     ```

   - Document MCP client configuration using the `linguamcp` command.
   - Document `--data-root` and `LINGUAMCP_DATA_ROOT`.
   - Keep repository-based development instructions separately.

5. Migration guidance.
   - Tell existing repo users that their old data may live under `<repo>/tutor_data`.
   - Do not auto-move existing data silently.
   - Provide a manual migration example:

     ```powershell
     Copy-Item -Recurse ".\tutor_data" "$env:USERPROFILE\LinguaMCP\tutor_data"
     ```

## Phase 2: Windows Launcher

Update the launcher after the server has stable data-root support.

1. Show the active data folder in the launcher UI.

   Example:

   ```text
   Data folder:
   C:\Users\hamza\LinguaMCP\tutor_data

   [Change...] [Open Folder]
   ```

2. Start the server with the selected data root.

   Example:

   ```powershell
   linguamcp --data-root "C:\Users\hamza\LinguaMCP\tutor_data" --http --oauth --allow-writes
   ```

3. Add `Open Folder`.
   - Opens the selected data root in File Explorer.
   - Useful because learner memory is intentionally file-based and inspectable.

4. Add `Change...`.
   - Lets non-terminal users choose a different data location.
   - Persist the selected folder in launcher settings.
   - The launcher should pass the selected folder as `--data-root`.

5. Optional later migration prompt.
   - If the launcher detects an existing repo-local `tutor_data/`, it can ask whether to use or copy that data folder.
   - This should be explicit, never silent.

## Suggested Implementation Order

1. Add `--data-root`, `LINGUAMCP_DATA_ROOT`, and default user-folder behavior.
2. Update audit log handling to derive from the configured data root.
3. Add tests for CLI/env/default data root behavior.
4. Restructure into a package and add `pyproject.toml`.
5. Update README and MCP client examples.
6. Update launcher UI and startup command.

