import tempfile
import unittest
from pathlib import Path

from src.web_runtime import TaskStore, is_allowed_path, parse_transform_level, validate_video_url


class WebRuntimeTests(unittest.TestCase):
    def test_validate_video_url_accepts_http_and_https(self):
        self.assertTrue(validate_video_url("https://www.youtube.com/watch?v=abc"))
        self.assertTrue(validate_video_url("http://example.com/video.mp4"))

    def test_validate_video_url_rejects_invalid_values(self):
        self.assertFalse(validate_video_url(""))
        self.assertFalse(validate_video_url("ftp://example.com/video.mp4"))
        self.assertFalse(validate_video_url("youtube.com/watch?v=abc"))

    def test_parse_transform_level_accepts_supported_values(self):
        self.assertEqual(parse_transform_level("2"), 2)
        self.assertEqual(parse_transform_level(None), 1)

    def test_parse_transform_level_rejects_invalid_values(self):
        with self.assertRaises(ValueError):
            parse_transform_level("9")

        with self.assertRaises(ValueError):
            parse_transform_level("abc")

    def test_is_allowed_path_limits_access_to_repo_and_output_roots(self):
        self.assertTrue(is_allowed_path(Path.cwd()))
        self.assertFalse(is_allowed_path("/tmp/not-openfang-safe"))

    def test_task_store_persists_updates(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tasks_file = Path(tmp_dir) / "tasks.json"
            store = TaskStore(tasks_file)
            store.create("task_1", ["python3", "demo.py"], metadata={"kind": "demo"})
            store.update("task_1", status="completed", output="ok")

            reloaded = TaskStore(tasks_file)
            task = reloaded.get("task_1")

            self.assertIsNotNone(task)
            self.assertEqual(task["status"], "completed")
            self.assertEqual(task["output"], "ok")
            self.assertEqual(task["kind"], "demo")


if __name__ == "__main__":
    unittest.main()
