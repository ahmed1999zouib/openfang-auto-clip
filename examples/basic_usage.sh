#!/bin/bash
# OpenFang Auto Clip - Basic Usage Examples

# Example 1: Simple video editing
echo "Example 1: Basic video editing"
./auto_clip.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --duration 30

# Example 2: With copyright transformation (Level 1)
echo "Example 2: Copyright-safe transformation (Level 1)"
./auto_clip.py "URL" --transform 1

# Example 3: Custom duration
echo "Example 3: 45-second clips"
./auto_clip.py "URL" --duration 45

# Example 4: Batch processing
echo "Example 4: Batch processing"
cat videos.txt | xargs -I {} ./auto_clip.py {}

# Example 5: With custom config
echo "Example 5: Using custom config"
./auto_clip.py "URL" --config my_config.json
