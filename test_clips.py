#!/usr/bin/env python3
"""
使用转换后的视频创建短视频片段
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime

def create_test_clips(video_path: str):
    """从转换后的视频创建测试片段"""

    print("=" * 70)
    print("🎬 从转换后视频创建短视频片段")
    print("=" * 70)
    print()

    # 创建输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path.home() / ".openfang" / "clips" / f"transformed_test_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 定义要提取的片段（从视频的不同时间段）
    clips = [
        {"start": 60, "end": 90, "name": "clip_01_开场"},
        {"start": 180, "end": 210, "name": "clip_02_高潮"},
        {"start": 300, "end": 330, "name": "clip_03_结尾"},
    ]

    created_clips = []

    for i, clip in enumerate(clips):
        start = clip["start"]
        end = clip["end"]
        duration = end - start
        name = clip["name"]
        output_path = output_dir / f"{name}.mp4"

        print(f"[{i+1}/{len(clips)}] 提取片段: {name}")
        print(f"    时间: {start}s - {end}s (时长: {duration}s)")

        # 使用FFmpeg提取片段并转换为9:16竖屏
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-ss", str(start),
            "-t", str(duration),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            "-y",
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"    ✅ {file_size:.1f} MB")
            created_clips.append({
                "name": name,
                "path": str(output_path),
                "start": start,
                "end": end,
                "size_mb": file_size
            })
        else:
            print(f"    ❌ 失败: {result.stderr[:100]}")

    # 生成报告
    print("\n" + "=" * 70)
    print("✅ 片段创建完成！")
    print("=" * 70)
    print(f"📁 输出目录: {output_dir}")
    print(f"📹 成功创建: {len(created_clips)} 个片段")
    print()

    for clip in created_clips:
        print(f"  • {clip['name']}: {clip['size_mb']:.1f} MB")
        print(f"    {clip['path']}")

    # 保存报告
    report = {
        "source_video": video_path,
        "clips": created_clips,
        "transformations_applied": [
            "horizontal_flip",
            "zoom_crop",
            "color_grading",
            "speed_1.15x",
            "rotation_1.5deg",
            "vignette",
            "noise_overlay",
            "pitch_shift"
        ],
        "created_at": datetime.now().isoformat()
    }

    report_path = output_dir / "report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)

    print()
    print("💡 下一步:")
    print(f"  1. 播放片段查看效果")
    print(f"  2. 上传到 TikTok/Shorts/Reels 测试")
    print()
    print(f"📂 打开目录: open {output_dir}")

    return output_dir

if __name__ == "__main__":
    # 使用转换后的视频
    video_path = "/Users/terre/.openfang/clips/downloads/babybus_transformed.mp4"

    output_dir = create_test_clips(video_path)

    # 打开输出目录
    import subprocess
    subprocess.run(["open", str(output_dir)])
