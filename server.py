"""FastMCP server for local, Markdown-backed language tutor memory."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from fastmcp import FastMCP
except ModuleNotFoundError:
    class FastMCP:  # type: ignore[no-redef]
        """Small import-time shim so storage verification can run before setup."""

        def __init__(self, name: str) -> None:
            self.name = name

        def tool(self, function: Any) -> Any:
            return function

        def run(self) -> None:
            raise RuntimeError(
                "FastMCP is not installed. Run: python -m pip install -r requirements.txt"
            )


PROJECT_ROOT = Path(__file__).resolve().parent
TUTOR_DATA_ROOT = PROJECT_ROOT / "tutor_data"
TEMPLATE_ROOT = PROJECT_ROOT / "templates"

CONTEXT_FILES = (
    "00-profile.md",
    "01-lesson-plan.md",
    "02-progress.md",
    "03-vocabulary.md",
    "04-mistakes.md",
    "05-scenarios.md",
    "latest-summary.md",
    "active-session.md",
    "latest-homework.md",
)

DELIVERY_FILES = (
    "delivery/latest-email.md",
    "delivery/latest-whatsapp.md",
)

ALLOWED_FILES = CONTEXT_FILES + DELIVERY_FILES

COMPACTABLE_FILES = (
    "00-profile.md",
    "01-lesson-plan.md",
    "02-progress.md",
    "03-vocabulary.md",
    "04-mistakes.md",
    "05-scenarios.md",
)

CONTEXT_COMPACTION_THRESHOLD_CHARS = 12_000
TOTAL_CONTEXT_COMPACTION_THRESHOLD_CHARS = 36_000

TEMPLATE_FILES = {
    "00-profile.md": "00-profile.md",
    "01-lesson-plan.md": "01-lesson-plan.md",
    "02-progress.md": "02-progress.md",
    "03-vocabulary.md": "03-vocabulary.md",
    "04-mistakes.md": "04-mistakes.md",
    "05-scenarios.md": "05-scenarios.md",
    "latest-summary.md": "latest-summary.md",
    "active-session.md": "active-session.md",
    "latest-homework.md": "latest-homework.md",
    "delivery/latest-email.md": "latest-email.md",
    "delivery/latest-whatsapp.md": "latest-whatsapp.md",
}

LANGUAGE_PATTERN = re.compile(r"^[a-z][a-z0-9-]{0,49}$")
TIMESTAMPED_MARKDOWN_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{6}Z\.md$"
)

mcp = FastMCP("Local Language Tutor Memory")


def _normalize_language(language: str) -> str:
    if not isinstance(language, str):
        raise ValueError("Language must be a string.")
    normalized = language.strip().lower()
    if not LANGUAGE_PATTERN.fullmatch(normalized):
        raise ValueError(
            "Invalid language. Use 1-50 lowercase letters, digits, or hyphens, "
            "starting with a letter."
        )
    return normalized


def _require_markdown(content: str, field_name: str = "content") -> str:
    if not isinstance(content, str):
        raise ValueError(f"{field_name} must be a string containing Markdown.")
    return content


def _safe_child(root: Path, *parts: str) -> Path:
    resolved_root = root.resolve()
    candidate = resolved_root.joinpath(*parts).resolve()
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError("Invalid path: access outside tutor_data is not allowed.")
    return candidate


def _language_directory(language: str, data_root: Path) -> tuple[str, Path]:
    normalized = _normalize_language(language)
    return normalized, _safe_child(data_root, normalized)


def _read_template(filename: str, template_root: Path) -> str:
    template_path = _safe_child(template_root, TEMPLATE_FILES[filename])
    try:
        return template_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"Required template is missing: {filename}") from exc


def _utc_filename(now: datetime | None = None) -> str:
    timestamp = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return timestamp.strftime("%Y-%m-%dT%H-%M-%S-%fZ.md")


def _validate_allowed_filename(filename: str) -> str:
    if not isinstance(filename, str) or filename not in ALLOWED_FILES:
        raise ValueError(
            "Invalid filename. Allowed files: " + ", ".join(ALLOWED_FILES)
        )
    return filename


def _require_language_profile(language: str, data_root: Path) -> tuple[str, Path]:
    normalized, language_dir = _language_directory(language, data_root)
    if not language_dir.is_dir():
        raise ValueError(f"Language profile does not exist: {normalized}")
    return normalized, language_dir


def initialize_profile(
    language: str,
    profile_markdown: str,
    lesson_plan_markdown: str,
    overwrite_existing: bool = False,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
    template_root: Path = TEMPLATE_ROOT,
) -> dict[str, Any]:
    """Create a language directory and its standard Markdown files."""
    normalized, language_dir = _language_directory(language, data_root)
    profile_markdown = _require_markdown(profile_markdown, "profile_markdown")
    lesson_plan_markdown = _require_markdown(
        lesson_plan_markdown, "lesson_plan_markdown"
    )

    language_dir.mkdir(parents=True, exist_ok=True)
    for directory in ("sessions", "delivery", "archives"):
        _safe_child(language_dir, directory).mkdir(exist_ok=True)

    supplied_content = {
        "00-profile.md": profile_markdown,
        "01-lesson-plan.md": lesson_plan_markdown,
    }
    created: list[str] = []
    overwritten: list[str] = []
    preserved: list[str] = []

    for filename in ALLOWED_FILES:
        path = _safe_child(language_dir, filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        content = supplied_content.get(filename)
        if content is None:
            content = _read_template(filename, template_root).replace(
                "{{language}}", normalized.title()
            )

        if path.exists():
            if filename in supplied_content and overwrite_existing:
                path.write_text(content, encoding="utf-8")
                overwritten.append(filename)
            else:
                preserved.append(filename)
            continue

        path.write_text(content, encoding="utf-8")
        created.append(filename)

    return {
        "language": normalized,
        "created": created,
        "overwritten": overwritten,
        "preserved": preserved,
        "directories": ["sessions", "delivery", "archives"],
    }


def read_context(
    language: str, *, data_root: Path = TUTOR_DATA_ROOT
) -> dict[str, str]:
    """Read the complete current Markdown context for a language."""
    normalized, language_dir = _require_language_profile(language, data_root)

    context: dict[str, str] = {"language": normalized}
    for filename in CONTEXT_FILES:
        path = _safe_child(language_dir, filename)
        if not path.is_file():
            raise ValueError(
                f"Language profile is incomplete; missing file: {filename}"
            )
        context[filename] = path.read_text(encoding="utf-8")
    return context


def write_file(
    language: str,
    filename: str,
    content: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
) -> dict[str, Any]:
    """Replace one whitelisted Markdown file for an existing language."""
    normalized, language_dir = _require_language_profile(language, data_root)
    filename = _validate_allowed_filename(filename)
    content = _require_markdown(content)

    path = _safe_child(language_dir, filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return {
        "language": normalized,
        "filename": filename,
        "characters_written": len(content),
    }


def append_session(
    language: str,
    session_markdown: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
    template_root: Path = TEMPLATE_ROOT,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create a timestamped session log and refresh latest-summary.md."""
    normalized, language_dir = _require_language_profile(language, data_root)
    session_markdown = _require_markdown(session_markdown, "session_markdown")

    sessions_dir = _safe_child(language_dir, "sessions")
    sessions_dir.mkdir(exist_ok=True)
    filename = _utc_filename(now)
    session_path = _safe_child(sessions_dir, filename)
    session_path.write_text(session_markdown, encoding="utf-8")

    latest_summary = _safe_child(language_dir, "latest-summary.md")
    latest_summary.write_text(session_markdown, encoding="utf-8")
    active_session = _safe_child(language_dir, "active-session.md")
    active_session.write_text(
        _read_template("active-session.md", template_root).replace(
            "{{language}}", normalized.title()
        ),
        encoding="utf-8",
    )
    return {
        "language": normalized,
        "session_file": f"sessions/{filename}",
        "latest_summary_updated": True,
        "active_session_cleared": True,
    }


def save_checkpoint(
    language: str,
    checkpoint_markdown: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
) -> dict[str, Any]:
    """Replace the bounded active-session checkpoint for a language."""
    normalized, language_dir = _require_language_profile(language, data_root)
    checkpoint_markdown = _require_markdown(
        checkpoint_markdown, "checkpoint_markdown"
    )
    path = _safe_child(language_dir, "active-session.md")
    path.write_text(checkpoint_markdown, encoding="utf-8")
    return {
        "language": normalized,
        "filename": "active-session.md",
        "characters_written": len(checkpoint_markdown),
    }


def context_status(
    language: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
    threshold_chars: int = CONTEXT_COMPACTION_THRESHOLD_CHARS,
    total_threshold_chars: int = TOTAL_CONTEXT_COMPACTION_THRESHOLD_CHARS,
) -> dict[str, Any]:
    """Report context sizes without interpreting or summarizing learner data."""
    normalized, language_dir = _require_language_profile(language, data_root)
    if threshold_chars < 1:
        raise ValueError("threshold_chars must be a positive integer.")
    if total_threshold_chars < 1:
        raise ValueError("total_threshold_chars must be a positive integer.")

    files: dict[str, dict[str, Any]] = {}
    total_characters = 0
    for filename in CONTEXT_FILES:
        path = _safe_child(language_dir, filename)
        if not path.is_file():
            raise ValueError(
                f"Language profile is incomplete; missing file: {filename}"
            )
        character_count = len(path.read_text(encoding="utf-8"))
        total_characters += character_count
        compactable = filename in COMPACTABLE_FILES
        files[filename] = {
            "characters": character_count,
            "compactable": compactable,
            "compaction_recommended": compactable
            and character_count >= threshold_chars,
        }

    recommended_files = [
        filename
        for filename, status in files.items()
        if status["compaction_recommended"]
    ]
    total_warning = total_characters >= total_threshold_chars
    if total_warning and not recommended_files:
        largest_compactable = max(
            COMPACTABLE_FILES,
            key=lambda filename: files[filename]["characters"],
        )
        files[largest_compactable]["compaction_recommended"] = True
        recommended_files.append(largest_compactable)

    return {
        "language": normalized,
        "threshold_characters": threshold_chars,
        "total_threshold_characters": total_threshold_chars,
        "total_context_characters": total_characters,
        "total_context_compaction_recommended": total_warning,
        "files": files,
        "files_recommended_for_compaction": recommended_files,
    }


def compact_file(
    language: str,
    filename: str,
    compacted_markdown: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Archive a cumulative context file and replace it with an AI summary."""
    normalized, language_dir = _require_language_profile(language, data_root)
    if not isinstance(filename, str) or filename not in COMPACTABLE_FILES:
        raise ValueError(
            "Invalid filename. Compactable files: "
            + ", ".join(COMPACTABLE_FILES)
        )
    compacted_markdown = _require_markdown(
        compacted_markdown, "compacted_markdown"
    )

    source_path = _safe_child(language_dir, filename)
    if not source_path.is_file():
        raise ValueError(f"Language profile is incomplete; missing file: {filename}")
    previous_content = source_path.read_text(encoding="utf-8")

    archive_directory = _safe_child(
        language_dir, "archives", filename.removesuffix(".md")
    )
    archive_directory.mkdir(parents=True, exist_ok=True)
    archive_filename = _utc_filename(now)
    archive_path = _safe_child(archive_directory, archive_filename)
    archive_path.write_text(previous_content, encoding="utf-8")
    source_path.write_text(compacted_markdown, encoding="utf-8")

    return {
        "language": normalized,
        "filename": filename,
        "archive_file": (
            f"archives/{filename.removesuffix('.md')}/{archive_filename}"
        ),
        "previous_characters": len(previous_content),
        "current_characters": len(compacted_markdown),
    }


def list_archives(
    language: str,
    filename: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
) -> list[str]:
    """List timestamped archives for one cumulative context file."""
    _, language_dir = _require_language_profile(language, data_root)
    if not isinstance(filename, str) or filename not in COMPACTABLE_FILES:
        raise ValueError(
            "Invalid filename. Archived files: " + ", ".join(COMPACTABLE_FILES)
        )
    archive_directory = _safe_child(
        language_dir, "archives", filename.removesuffix(".md")
    )
    if not archive_directory.exists():
        return []
    return sorted(
        path.name
        for path in archive_directory.iterdir()
        if path.is_file() and TIMESTAMPED_MARKDOWN_PATTERN.fullmatch(path.name)
    )


def read_archive(
    language: str,
    filename: str,
    archive_filename: str,
    *,
    data_root: Path = TUTOR_DATA_ROOT,
) -> dict[str, str]:
    """Read one validated timestamped archive without loading all history."""
    normalized, language_dir = _require_language_profile(language, data_root)
    if not isinstance(filename, str) or filename not in COMPACTABLE_FILES:
        raise ValueError(
            "Invalid filename. Archived files: " + ", ".join(COMPACTABLE_FILES)
        )
    if not isinstance(archive_filename, str) or not (
        TIMESTAMPED_MARKDOWN_PATTERN.fullmatch(archive_filename)
    ):
        raise ValueError("Invalid archive filename. Use a value returned by list archives.")
    archive_path = _safe_child(
        language_dir,
        "archives",
        filename.removesuffix(".md"),
        archive_filename,
    )
    if not archive_path.is_file():
        raise ValueError(f"Archive does not exist: {archive_filename}")
    return {
        "language": normalized,
        "filename": filename,
        "archive_filename": archive_filename,
        "content": archive_path.read_text(encoding="utf-8"),
    }


def available_languages(*, data_root: Path = TUTOR_DATA_ROOT) -> list[str]:
    """List valid language profile directories in alphabetical order."""
    if not data_root.exists():
        return []
    languages = [
        path.name
        for path in data_root.iterdir()
        if path.is_dir() and LANGUAGE_PATTERN.fullmatch(path.name)
    ]
    return sorted(languages)


@mcp.tool
def initialize_language_profile(
    language: str,
    profile_markdown: str,
    lesson_plan_markdown: str,
    overwrite_existing: bool = False,
) -> dict[str, Any]:
    """Initialize local Markdown memory for a language.

    Existing profile and lesson-plan files are preserved unless
    overwrite_existing is explicitly true. Other existing files are never reset.
    """
    return initialize_profile(
        language, profile_markdown, lesson_plan_markdown, overwrite_existing
    )


@mcp.tool
def read_language_context(language: str) -> dict[str, str]:
    """Read the bounded active tutor context, excluding archives and drafts."""
    return read_context(language)


@mcp.tool
def write_language_file(
    language: str, filename: str, content: str
) -> dict[str, Any]:
    """Replace one allowed Markdown file in an existing language profile."""
    return write_file(language, filename, content)


@mcp.tool
def append_session_log(language: str, session_markdown: str) -> dict[str, Any]:
    """Save a final session, update latest summary, and clear the checkpoint."""
    return append_session(language, session_markdown)


@mcp.tool
def save_session_checkpoint(
    language: str, checkpoint_markdown: str
) -> dict[str, Any]:
    """Overwrite the concise active-session checkpoint during a long lesson."""
    return save_checkpoint(language, checkpoint_markdown)


@mcp.tool
def get_language_context_status(language: str) -> dict[str, Any]:
    """Report context sizes and cumulative files recommended for compaction."""
    return context_status(language)


@mcp.tool
def compact_language_file(
    language: str, filename: str, compacted_markdown: str
) -> dict[str, Any]:
    """Archive one cumulative context file and replace it with a concise version."""
    return compact_file(language, filename, compacted_markdown)


@mcp.tool
def list_language_file_archives(language: str, filename: str) -> list[str]:
    """List available archive timestamps for one cumulative context file."""
    return list_archives(language, filename)


@mcp.tool
def read_language_file_archive(
    language: str, filename: str, archive_filename: str
) -> dict[str, str]:
    """Read one archive selected from list_language_file_archives."""
    return read_archive(language, filename, archive_filename)


@mcp.tool
def list_languages() -> list[str]:
    """List initialized language profiles."""
    return available_languages()


if __name__ == "__main__":
    mcp.run()
