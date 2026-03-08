import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import release_prep


class ReleasePrepTests(unittest.TestCase):
    def test_validate_version_accepts_plain_and_prefixed_versions(self):
        self.assertEqual(release_prep.validate_version("0.3.0"), "0.3.0")
        self.assertEqual(release_prep.validate_version("v0.3.0"), "0.3.0")

    def test_validate_version_rejects_invalid_versions(self):
        with self.assertRaises(ValueError):
            release_prep.validate_version("0.3")

    def test_extract_changelog_section_prefers_matching_version(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            (repo_root / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n- future\n\n## [0.3.0]\n- shipped\n\n## [0.2.0]\n- older\n"
            )
            with mock.patch.object(release_prep, "REPO_ROOT", repo_root):
                section = release_prep.extract_changelog_section("0.3.0")

        self.assertIn("shipped", section)
        self.assertNotIn("older", section)

    def test_write_release_bundle_creates_notes_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            notes_path = release_prep.write_release_bundle("0.3.0", "# Demo", output_dir)

            self.assertTrue(notes_path.exists())
            self.assertEqual(notes_path.read_text(), "# Demo")


if __name__ == "__main__":
    unittest.main()
