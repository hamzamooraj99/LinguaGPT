# Contributing to LinguaMCP

Thank you for contributing. LinguaMCP is intentionally small: it is a
filesystem-backed MCP memory layer, while teaching behavior belongs to the
connected language model.

## Before opening a change

For bug fixes and small documentation improvements, open a pull request
directly. For new tools, storage-format changes, new dependencies, or changes
to the project architecture, open an issue first so the scope can be agreed.

Do not include learner data, credentials, access tokens, logs, generated build
artifacts, or local environment files in an issue or pull request.

## Development setup

LinguaMCP requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The optional Windows launcher targets .NET 9 and WPF.

## Making changes

- Keep storage under `tutor_data/` and use UTF-8 Markdown as the source of truth.
- Keep teaching, assessment, and curriculum decisions out of the MCP server.
- Validate all external input and prevent writes outside `tutor_data/`.
- Prefer `pathlib`, type hints, small functions, and minimal dependencies.
- Keep each MCP tool focused on one responsibility.
- Preserve existing user data unless a migration has been explicitly designed.
- Add or update tests for behavior changes.

## Verification

Run the complete test suite before submitting a pull request:

```powershell
python -m unittest discover -s tests -v
```

Changes involving storage must verify successful execution, correct file
creation, path-traversal rejection, and UTF-8 preservation. Launcher changes
should also be built with:

```powershell
dotnet build launcher/LinguaMCP.Launcher.csproj
```

## Pull requests

Keep pull requests focused. Include:

- a concise description of the problem and solution
- relevant issue links
- tests performed and their results
- security or compatibility implications

By contributing, you agree that your contribution is licensed under the GNU
General Public License v3.0 included in this repository. All participants must
follow the
[Code of Conduct](CODE_OF_CONDUCT.md).
