from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from server import (
    ALLOWED_FILES,
    append_session,
    available_languages,
    compact_file,
    context_status,
    initialize_profile,
    list_archives,
    read_context,
    read_archive,
    save_checkpoint,
    write_file,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class StorageVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.data_root = Path(self.temporary_directory.name) / "tutor_data"
        self.template_root = PROJECT_ROOT / "templates"

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def initialize(self) -> dict[str, object]:
        return initialize_profile(
            "German",
            "# Profil\n\nIch lerne Deutsch. Grüße!",
            "# Plan\n\nÜbe täglich.",
            data_root=self.data_root,
            template_root=self.template_root,
        )

    def test_initialization_creates_complete_profile_and_preserves_existing(self) -> None:
        result = self.initialize()
        language_dir = self.data_root / "german"

        self.assertEqual(set(result["created"]), set(ALLOWED_FILES))
        self.assertTrue((language_dir / "sessions").is_dir())
        self.assertTrue((language_dir / "delivery").is_dir())
        self.assertTrue((language_dir / "archives").is_dir())
        for filename in ALLOWED_FILES:
            self.assertTrue((language_dir / filename).is_file())

        self.initialize()
        self.assertIn("Grüße", (language_dir / "00-profile.md").read_text("utf-8"))

        initialize_profile(
            "german",
            "# Replaced profile",
            "# Replaced plan",
            True,
            data_root=self.data_root,
            template_root=self.template_root,
        )
        self.assertEqual(
            (language_dir / "00-profile.md").read_text("utf-8"),
            "# Replaced profile",
        )

    def test_read_context_and_utf8(self) -> None:
        self.initialize()
        context = read_context("german", data_root=self.data_root)

        self.assertEqual(context["language"], "german")
        self.assertIn("Grüße", context["00-profile.md"])
        self.assertEqual(len(context), 10)
        self.assertNotIn("delivery/latest-email.md", context)

    def test_write_allowed_file(self) -> None:
        self.initialize()
        write_file(
            "german",
            "02-progress.md",
            "# Fortschritt\n\nSchön!",
            data_root=self.data_root,
        )
        self.assertIn(
            "Schön",
            read_context("german", data_root=self.data_root)["02-progress.md"],
        )

    def test_invalid_paths_and_filenames_are_rejected(self) -> None:
        self.initialize()
        invalid_languages = ("../outside", "german/../../outside", "C:\\temp")
        for language in invalid_languages:
            with self.subTest(language=language), self.assertRaises(ValueError):
                read_context(language, data_root=self.data_root)

        for filename in (
            "../notes.md",
            "sessions/evil.md",
            "delivery/../../evil.md",
            "notes.txt",
        ):
            with self.subTest(filename=filename), self.assertRaises(ValueError):
                write_file("german", filename, "bad", data_root=self.data_root)

    def test_session_log_is_timestamped_and_updates_latest_summary(self) -> None:
        self.initialize()
        summary = "# Zusammenfassung\n\nHeute: Grüße und Café."
        fixed_time = datetime(2026, 6, 21, 10, 11, 12, 123456, tzinfo=timezone.utc)

        result = append_session(
            "german",
            summary,
            data_root=self.data_root,
            template_root=self.template_root,
            now=fixed_time,
        )
        expected = "sessions/2026-06-21T10-11-12-123456Z.md"

        self.assertEqual(result["session_file"], expected)
        self.assertEqual(
            (self.data_root / "german" / expected).read_text("utf-8"), summary
        )
        self.assertEqual(
            (self.data_root / "german" / "latest-summary.md").read_text("utf-8"),
            summary,
        )
        self.assertIn(
            "No active session checkpoint",
            (self.data_root / "german" / "active-session.md").read_text("utf-8"),
        )
        self.assertEqual(available_languages(data_root=self.data_root), ["german"])

    def test_checkpoint_is_bounded_and_delivery_drafts_are_writable(self) -> None:
        self.initialize()
        first = "# Checkpoint\n\nFirst state"
        second = "# Checkpoint\n\nCurrent state"
        save_checkpoint("german", first, data_root=self.data_root)
        save_checkpoint("german", second, data_root=self.data_root)
        write_file(
            "german",
            "delivery/latest-whatsapp.md",
            "Homework: review greetings.",
            data_root=self.data_root,
        )

        language_dir = self.data_root / "german"
        self.assertEqual(
            (language_dir / "active-session.md").read_text("utf-8"), second
        )
        self.assertEqual(
            (language_dir / "delivery" / "latest-whatsapp.md").read_text(
                "utf-8"
            ),
            "Homework: review greetings.",
        )

    def test_context_status_and_compaction_preserve_full_archive(self) -> None:
        self.initialize()
        original = "# Vocabulary\n\n" + ("Wort — word\n" * 20)
        compacted = "# Vocabulary\n\n- Wort — word"
        write_file(
            "german", "03-vocabulary.md", original, data_root=self.data_root
        )

        status = context_status(
            "german", data_root=self.data_root, threshold_chars=100
        )
        self.assertIn(
            "03-vocabulary.md", status["files_recommended_for_compaction"]
        )

        fixed_time = datetime(2026, 6, 21, 12, 0, 0, 0, tzinfo=timezone.utc)
        result = compact_file(
            "german",
            "03-vocabulary.md",
            compacted,
            data_root=self.data_root,
            now=fixed_time,
        )
        archive_path = self.data_root / "german" / result["archive_file"]

        self.assertEqual(archive_path.read_text("utf-8"), original)
        self.assertEqual(
            (self.data_root / "german" / "03-vocabulary.md").read_text("utf-8"),
            compacted,
        )
        archive_name = Path(result["archive_file"]).name
        self.assertEqual(
            list_archives(
                "german", "03-vocabulary.md", data_root=self.data_root
            ),
            [archive_name],
        )
        self.assertEqual(
            read_archive(
                "german",
                "03-vocabulary.md",
                archive_name,
                data_root=self.data_root,
            )["content"],
            original,
        )

        total_status = context_status(
            "german",
            data_root=self.data_root,
            threshold_chars=1_000_000,
            total_threshold_chars=1,
        )
        self.assertTrue(total_status["total_context_compaction_recommended"])
        self.assertEqual(len(total_status["files_recommended_for_compaction"]), 1)

        with self.assertRaises(ValueError):
            compact_file(
                "german",
                "latest-summary.md",
                "not allowed",
                data_root=self.data_root,
            )
        with self.assertRaises(ValueError):
            read_archive(
                "german",
                "03-vocabulary.md",
                "../outside.md",
                data_root=self.data_root,
            )


if __name__ == "__main__":
    unittest.main()
