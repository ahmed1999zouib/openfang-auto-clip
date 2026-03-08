import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock

import auto_clip


class AutoClipCliTests(unittest.TestCase):
    def test_build_processing_plan_contains_expected_fields(self):
        config = {"default_duration": 45, "target_platforms": ["tiktok", "shorts"]}
        plan = auto_clip.build_processing_plan(
            "https://example.com/video",
            1,
            config,
            now=datetime(2026, 3, 8, 12, 0, 0),
        )

        self.assertEqual(plan["transform_label"], "visual")
        self.assertEqual(plan["default_duration"], 45)
        self.assertIn("20260308_120000", plan["projected_output_dir"])

    def test_save_dry_run_plan_writes_json_file(self):
        plan = {"url": "https://example.com/video", "transform_level": 1}

        with tempfile.TemporaryDirectory() as tmp_dir:
            with mock.patch.object(auto_clip, "OUTPUT_DIR", Path(tmp_dir)):
                plan_path = auto_clip.save_dry_run_plan(plan)

            self.assertTrue(plan_path.exists())
            self.assertEqual(plan_path.parent.name, "dry_runs")

    def test_build_doctor_report_marks_required_tools_missing(self):
        with mock.patch.object(auto_clip, "command_exists", side_effect=lambda cmd: cmd == "ffmpeg"):
            with mock.patch("auto_clip.shutil.which", side_effect=lambda cmd: f"/usr/bin/{cmd}" if cmd == "ffmpeg" else None):
                report = auto_clip.build_doctor_report()

        statuses = {check["name"]: check["status"] for check in report["checks"]}
        self.assertEqual(statuses["ffmpeg"], "ok")
        self.assertEqual(statuses["yt-dlp"], "error")
        self.assertIn(statuses["openfang"], {"warn", "ok"})


if __name__ == "__main__":
    unittest.main()
