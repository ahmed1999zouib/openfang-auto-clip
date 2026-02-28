#!/usr/bin/env python3
"""
测试版权转换效果
"""

import os
import sys
import subprocess
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from auto_clip import CopyrightTransformer, load_config

def transform_existing_video(video_path: str, level: int = 1):
    """对已有视频进行版权转换"""

    print("=" * 70)
    print("🎬 测试版权转换效果")
    print("=" * 70)
    print(f"📁 视频文件: {video_path}")
    print(f"📦 文件大小: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    print()

    # 加载配置
    config = load_config()

    # 创建转换器
    transformer = CopyrightTransformer(config)

    # 执行转换
    from auto_clip import TransformLevel
    result = transformer.transform(video_path, TransformLevel(level))

    print("\n" + "=" * 70)
    if result.get('status') == 'success':
        print("✅ 转换成功！")
        print("=" * 70)
        output_path = result.get('output_path')
        print(f"📁 输出文件: {output_path}")
        print(f"📦 文件大小: {result.get('file_size_mb', 0):.1f} MB")
        print(f"🛡️ 转换级别: Level {result.get('level')}")
        print("\n应用的转换效果:")
        for transform in result.get('transformations', []):
            print(f"  • {transform}")
        print()
        print("💡 下一步:")
        print(f"  1. 播放原视频和转换后视频对比效果")
        print(f"  2. 使用转换后的视频进行剪辑")
        print()
        print(f"📂 打开文件所在目录:")
        print(f"  open {Path(output_path).parent}")
        print()
    else:
        print("❌ 转换失败")
        print("=" * 70)
        print(f"错误信息: {result.get('message')}")

    return result

if __name__ == "__main__":
    # 使用之前下载的babybus视频
    video_path = "/Users/terre/.openfang/clips/downloads/babybus.mp4"

    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        sys.exit(1)

    # Level 1 转换
    result = transform_existing_video(video_path, level=1)

    if result.get('status') == 'success':
        sys.exit(0)
    else:
        sys.exit(1)
