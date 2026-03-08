# Benchmark Demo

This benchmark uses synthetic media, so anyone can reproduce the pipeline without downloading copyrighted source videos.

## What it does

- generates a short synthetic source video with `ffmpeg`
- optionally applies Level 1 transformation
- cuts the result into vertical clips
- writes a benchmark report and preview frame

## Run it

```bash
python3 scripts/run_demo_benchmark.py
```

## Output

```text
tmp/demo-benchmark/
├── benchmark_report.json
├── preview.png
├── synthetic_source.mp4
└── clips/
    ├── clip_01_0000s-0006s.mp4
    ├── clip_02_0006s-0012s.mp4
    └── clip_03_0012s-0018s.mp4
```

## Sample benchmark report

See [`sample_benchmark_report.json`](sample_benchmark_report.json).

The committed sample is illustrative. Running the script locally will generate a fresh report with your machine's timings.
