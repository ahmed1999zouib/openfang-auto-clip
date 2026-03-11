# Web Manager Guide

## Quick start

### Option 1

```bash
./start_web_manager.sh
```

### Option 2

```bash
source venv/bin/activate
python3 web_manager.py
```

The local UI opens at `http://localhost:5000`.

## What the interface covers

- IP character generation helpers
- local transformation and clip creation tasks
- Level 3 project-package generation
- URL-based video processing
- live task status and logs

## Intended workflow

1. enter a source URL or start with local test actions
2. choose the transformation level
3. launch the task
4. monitor progress in the log panel
5. inspect outputs in `~/.openfang`

## Runtime behavior

- tasks run in the background
- task metadata persists to `~/.openfang/web_tasks.json`
- the app resolves the current project root automatically
- `OPENFANG_AUTO_CLIP_PROJECT_DIR` can override the repo path
- `OPENFANG_OUTPUT_DIR` can override the output base directory

## Output locations

- IP assets: `~/.openfang/ip_characters/`
- downloaded media: `~/.openfang/clips/downloads/`
- generated clips: `~/.openfang/clips/<timestamp>/`
- transformed files: `~/.openfang/clips/transformed/`

## Troubleshooting

### Port conflict

Change the port in `web_manager.py` if `5000` is already taken.

### Missing Flask

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Missing virtualenv

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Positioning

The web manager is a local operator console. It is useful for demos and daily operation, but it is not a hosted SaaS control plane.
