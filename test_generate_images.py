#!/usr/bin/env python3
"""
本地测试IP角色生成 - 使用免费API
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# 检查是否有可用的API
HAS_OPENAI = False
try:
    import openai
    HAS_OPENAI = True
except:
    pass

def check_free_apis():
    """检查可用的免费API"""
    print("=" * 70)
    print("🔍 检查可用的AI服务")
    print("=" * 70)
    print()

    # 检查OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OpenAI API Key 已配置")
        print("   可以使用 DALL-E 3 生成高质量图片")
        print(f"   费用: 约 $0.04/张")
        print()
        return {"openai": True, "key": openai_key}
    else:
        print("❌ OpenAI API Key 未配置")
        print()
        print("💡 免费替代方案：")
        print("   1. Bing Image Creator - 完全免费")
        print("   2. Adobe Firefly - 免费25积分/月")
        print("   3. Stable Diffusion 本地 - 完全免费")
        print()
        return {"openai": False}

def generate_with_openai(api_key: str, prompts: list, output_dir: Path):
    """使用OpenAI DALL-E 3生成图片"""
    if not HAS_OPENAI:
        print("❌ 需要安装 openai 包:")
        print("   pip install openai")
        return False

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)

        print("=" * 70)
        print("🎨 使用 DALL-E 3 生成角色图片")
        print("=" * 70)
        print()

        generated = []

        for i, prompt_data in enumerate(prompts[:3], 1):  # 先生成3张测试
            name = prompt_data['name']
            prompt = prompt_data['prompt']

            print(f"[{i}/{len(prompts[:3])}] 生成: {name}")
            print(f"   提示词: {prompt[:80]}...")

            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )

                image_url = response.data[0].url

                # 下载图片
                import requests
                img_response = requests.get(image_url)
                if img_response.status_code == 200:
                    output_file = output_dir / f"{name}.png"
                    with open(output_file, 'wb') as f:
                        f.write(img_response.content)

                    file_size = output_file.stat().st_size / 1024
                    print(f"   ✅ 已保存: {file_size:.1f} KB")
                    generated.append(str(output_file))
                else:
                    print(f"   ❌ 下载失败")

            except Exception as e:
                print(f"   ❌ 生成失败: {e}")

            print()

        return generated

    except Exception as e:
        print(f"❌ OpenAI 调用失败: {e}")
        return False

def open_free_tools():
    """打开免费AI工具"""
    print("=" * 70)
    print("🌐 打开免费AI生成工具")
    print("=" * 70)
    print()

    tools = [
        ("Bing Image Creator", "https://www.bing.com/create"),
        ("Adobe Firefly", "https://firefly.adobe.com"),
        ("Craiyon", "https://www.craiyon.com"),
    ]

    print("正在打开浏览器...")
    for name, url in tools:
        print(f"   • {name}: {url}")
        subprocess.run(["open", url])

    print()
    print("💡 使用步骤：")
    print("   1. 在打开的网页中")
    print("   2. 复制下面的提示词")
    print("   3. 粘贴到输入框")
    print("   4. 点击生成")
    print("   5. 下载图片")
    print()

def show_test_prompts():
    """显示测试用的提示词"""
    test_prompts = [
        {
            "name": "消防员小狗Spike_正面",
            "prompt": "A cute cartoon golden retriever puppy wearing orange firefighter uniform and blue firefighter hat, friendly smile, waving hand, 3D Pixar style, bright colors, educational animation character"
        },
        {
            "name": "消防员小狗Spike_教学",
            "prompt": "Cartoon golden retriever puppy in firefighter uniform, teaching gesture, pointing at whiteboard, friendly expression, 3D animation style, educational character"
        },
        {
            "name": "消防员小狗Spike_Logo",
            "prompt": "Cartoon golden retriever puppy firefighter, portrait, head and shoulders, professional headshot, orange uniform, blue hat, 3D style, branding logo"
        }
    ]

    print("=" * 70)
    print("📝 测试提示词（点击复制）")
    print("=" * 70)
    print()

    for i, p in enumerate(test_prompts, 1):
        print(f"{i}. {p['name']}")
        print(f"   {p['prompt']}")
        print()

def create_demo_images(output_dir: Path):
    """创建演示用的占位图片"""
    print("=" * 70)
    print("🎨 创建演示占位图")
    print("=" * 70)
    print()

    # 使用ImageMagick创建简单的占位图
    for i in range(1, 4):
        output_file = output_dir / f"demo_character_{i}.png"

        # 创建一个简单的占位图
        cmd = [
            "convert",
            "-size", "1024x1024",
            "xc:lightblue",
            "-pointsize", "72",
            "-fill", "darkblue",
            "-gravity", "center",
            "-annotate", "+0+0",
            f"消防员小狗 Spike\\n角色占位图 #{i}\\n\\n使用下方工具生成实际图片",
            output_file
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ 创建占位图: {output_file.name}")
        except:
            print(f"⚠️ 无法创建占位图（需要安装ImageMagick）")

    print()

def main():
    """主测试函数"""
    print("=" * 70)
    print("🎬 本地测试 - IP角色生成")
    print("=" * 70)
    print()

    # 创建输出目录
    output_dir = Path.home() / ".openfang" / "ip_characters" / "test_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载角色包
    character_package_path = Path.home() / ".openfang" / "ip_characters" / "20260228_141454" / "character_package.json"

    if character_package_path.exists():
        with open(character_package_path) as f:
            package = json.load(f)
            prompts = package.get('prompts', [])
    else:
        print("⚠️ 未找到角色包，使用默认提示词")
        prompts = []

    # 检查API
    api_status = check_free_apis()

    # 如果有OpenAI API，使用它生成
    if api_status.get('openai') and prompts:
        generated = generate_with_openai(api_status['key'], prompts, output_dir)

        if generated:
            print("=" * 70)
            print("✅ 生成完成！")
            print("=" * 70)
            print(f"📁 位置: {output_dir}")
            print(f"🖼️  生成: {len(generated)} 张图片")
            print()
            subprocess.run(["open", output_dir])
            return

    # 如果没有API，使用免费工具
    print("=" * 70)
    print("💡 使用免费AI工具")
    print("=" * 70)
    print()

    # 创建占位图
    create_demo_images(output_dir)

    # 显示测试提示词
    show_test_prompts()

    # 打开免费工具
    open_free_tools()

    # 保存提示词到文件
    prompts_file = output_dir / "test_prompts.txt"
    with open(prompts_file, 'w', encoding='utf-8') as f:
        f.write("IP角色生成测试提示词\n")
        f.write("=" * 50 + "\n\n")
        f.write("将以下提示词复制到 Bing Image Creator 或其他免费工具：\n\n")
        for i in range(1, 4):
            f.write(f"\n图片 {i}:\n")
            f.write(f"{test_prompt := 'A cute cartoon golden retriever puppy wearing orange firefighter uniform and blue firefighter hat, friendly smile, 3D Pixar style, bright colors'}\n")
            f.write(f"{test_prompt}\n\n")

    print(f"✅ 测试提示词已保存到: {prompts_file}")
    print()
    print("=" * 70)
    print("📂 打开测试目录")
    print("=" * 70)
    print(f"📁 {output_dir}")
    print()
    subprocess.run(["open", output_dir])

    print()
    print("💡 下一步：")
    print("   1. 查看打开的免费AI工具网站")
    print("   2. 复制上面的提示词")
    print("   3. 粘贴并生成图片")
    print("   4. 下载到测试目录")
    print()

if __name__ == "__main__":
    main()
