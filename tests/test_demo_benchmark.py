import tempfile
import unittest
from pathlib import Path

from scripts import run_demo_benchmark


class DemoBenchmarkTests(unittest.TestCase):
    def test_build_highlights_splits_duration_evenly(self):
        highlights = run_demo_benchmark.build_highlights(18, 6)
        self.assertEqual(len(highlights), 3)
        self.assertEqual(highlights[0]["start"], 0)
        self.assertEqual(highlights[-1]["end"], 18)

    def test_build_highlights_handles_remainder(self):
        highlights = run_demo_benchmark.build_highlights(14, 6)
        self.assertEqual(len(highlights), 3)
        self.assertEqual(highlights[-1]["end"], 14)

    def test_run_benchmark_writes_report(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)

            def fake_source(output_path: Path, duration: int) -> None:
                output_path.write_bytes(b"source")

            def fake_extract_preview(video_path: Path, output_path: Path) -> None:
                output_path.write_bytes(b"preview")

            with unittest.mock.patch.object(run_demo_benchmark, "ensure_ffmpeg"):
                with unittest.mock.patch.object(run_demo_benchmark, "generate_synthetic_source", side_effect=fake_source):
                    with unittest.mock.patch.object(run_demo_benchmark, "extract_preview_frame", side_effect=fake_extract_preview):
                        with unittest.mock.patch.object(
                            run_demo_benchmark,
                            "create_clips",
                            return_value=[
                                {
                                    "path": str(output_dir / "clips" / "clip_01.mp4"),
                                    "start": 0,
                                    "end": 6,
                                    "duration": 6,
                                    "size_mb": 1.0,
                                    "reason": "Benchmark clip 1",
                                    "score": 5,
                                }
                            ],
                        ):
                            report = run_demo_benchmark.run_benchmark(output_dir, 18, 0, 6)

            self.assertEqual(report["artifacts"]["clip_count"], 1)
            self.assertTrue((output_dir / "benchmark_report.json").exists())


if __name__ == "__main__":
    unittest.main()
