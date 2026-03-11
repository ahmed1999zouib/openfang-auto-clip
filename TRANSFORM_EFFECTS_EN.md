# Transformation Effects Reference

## Current Level 1 profile

The project's enhanced `Level 1` transformation uses a stacked FFmpeg pipeline rather than a single cosmetic filter.

## Included effects

1. horizontal flip
2. scale and crop adjustment
3. slight rotation
4. color grading and contrast curve changes
5. playback speed adjustment
6. vignette
7. light dithering / grain
8. audio pitch shift

## Why this matters

Compared with a basic mirror-and-speed-change workflow, the current profile creates a visibly more distinct output and raises the cost of naive duplicate detection.

## What it does not guarantee

- it does not make copyrighted characters safe
- it does not convert copied media into fully original work
- it does not remove the need for platform testing and legal judgement

## Recommended use cases

- commentary
- educational remix
- short excerpts with added context
- internal prototyping

## Avoid using it for

- full-episode reuploads
- pretending source material is original
- commercial release of character-driven copyrighted media

## Typical workflow

```bash
./auto_clip.sh "URL" --transform 1 --duration 30
```

Or use the benchmark-safe path:

```bash
python3 scripts/run_demo_benchmark.py
```

## Output expectation

You should see:

- transformed media output
- vertical short clips
- benchmark or run report
- preview and storyboard assets in the demo workflow

## Bottom line

`Level 1` is a practical remix layer. It improves differentiation, but it should be positioned honestly as a lower-risk transformation step, not a full copyright solution.
