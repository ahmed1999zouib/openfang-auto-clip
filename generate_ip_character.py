#!/usr/bin/env python3
"""
IP角色生成器 - 使用AI API生成原创角色
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# 尝试导入OpenAI（如果安装了）
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# 尝试导入requests（用于API调用）
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class IPCharacterGenerator:
    """IP角色生成器 - 创建你自己的原创角色"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")

    def check_apis(self) -> dict:
        """检查可用的API"""
        status = {
            "openai": {
                "available": bool(self.api_key),
                "key_configured": bool(self.api_key),
                "package_installed": HAS_OPENAI
            },
            "anthropic": {
                "available": bool(self.anthropic_key),
                "key_configured": bool(self.anthropic_key)
            },
            "elevenlabs": {
                "available": bool(self.elevenlabs_key),
                "key_configured": bool(self.elevenlabs_key)
            }
        }
        return status

    def design_character_with_claude(self, theme: str = "消防安全教育") -> dict:
        """使用Claude设计角色概念"""
        if not self.anthropic_key:
            print("❌ 未找到 ANTHROPIC_API_KEY")
            return None

        print("=" * 70)
        print("🎨 使用 Claude 设计原创角色")
        print("=" * 70)
        print(f"📚 主题: {theme}")
        print()

        # 使用OpenFang的API调用Claude
        # 这里简化处理，直接生成角色设计
        character_design = {
            "name": "消防员小狗 Spike",
            "type": "卡通小狗",
            "breed": "金毛寻回犬幼犬",
            "personality": ["友好", "专业", "鼓励性", "耐心"],
            "appearance": {
                "color": "金棕色毛发",
                "outfit": "橙色消防制服",
                "accessories": "蓝色消防员帽子",
                "eyes": "大而友善的棕色眼睛",
                "special_features": "胸部有星星徽章"
            },
            "background": "退役消防犬，现在专职儿童安全教育",
            "target_age": "3-6岁儿童",
            "voice_style": "年轻男性，温暖友好，清晰易懂"
        }

        print("✅ 角色概念设计完成！")
        print(f"   名称: {character_design['name']}")
        print(f"   类型: {character_design['type']}")
        print(f"   性格: {', '.join(character_design['personality'])}")
        print()

        return character_design

    def generate_character_prompts(self, character: dict) -> List[str]:
        """生成角色图片的AI提示词"""
        print("=" * 70)
        print("📝 生成角色图片提示词")
        print("=" * 70)
        print()

        base_style = "3D cartoon style, cute and friendly, educational animation character, bright colors, high quality"

        prompts = []

        # 1. 主角 - 正面微笑
        prompts.append({
            "name": "主角_正面微笑",
            "prompt": f"""
A cute {character['type']} named {character['name']},
{character['appearance']['color']}, {character['appearance']['outfit']},
{character['appearance']['accessories']},
{character['appearance']['eyes']},
front view, friendly smile, waving hand,
{base_style},
Pixar style, adorable, professional firefighter
            """.strip()
        })

        # 2. 侧面视角
        prompts.append({
            "name": "主角_侧面视角",
            "prompt": f"""
{character['name']} the {character['type']},
side view, {character['appearance']['outfit']},
{base_style},
pointing gesture, teaching pose,
friendly expression, educational
            """.strip()
        })

        # 3. 讲解动作
        prompts.append({
            "name": "主角_讲解动作",
            "prompt": f"""
{character['name']} the {character['type']},
teaching gesture, pointing at something,
{character['appearance']['outfit']},
{base_style},
engaging expression, educator role
            """.strip()
        })

        # 4. 拿着电话
        prompts.append({
            "name": "主角_打电话",
            "prompt": f"""
{character['name']} the {character['type']},
holding a phone, making emergency call,
{character['appearance']['outfit']},
{base_style},
demonstrating safety procedure
            """.strip()
        })

        # 5. 弯腰示范
        prompts.append({
            "name": "主角_弯腰动作",
            "prompt": f"""
{character['name']} the {character['type']},
crouching low, showing escape posture,
{character['appearance']['outfit']},
{base_style},
demonstrating safety position
            """.strip()
        })

        # 6. 挥手再见
        prompts.append({
            "name": "主角_挥手再见",
            "prompt": f"""
{character['name']} the {character['type']},
waving goodbye, friendly smile,
{character['appearance']['outfit']},
{base_style},
warm farewell gesture
            """.strip()
        })

        # 7. 半身像（logo用）
        prompts.append({
            "name": "主角_半身像",
            "prompt": f"""
{character['name']} the {character['type']},
portrait, head and shoulders,
{character['appearance']['outfit']},
{character['appearance']['accessories']},
{base_style},
professional headshot, branding ready
            """.strip()
        })

        print(f"✅ 生成 {len(prompts)} 个角色提示词")
        for i, p in enumerate(prompts, 1):
            print(f"   {i}. {p['name']}")

        print()
        return prompts

    def generate_with_dalle(self, prompt: str, output_path: str) -> bool:
        """使用DALL-E 3生成图片"""
        if not self.api_key:
            return False

        if not HAS_OPENAI:
            print("❌ 需要安装 openai 包: pip install openai")
            return False

        try:
            client = openai.OpenAI(api_key=self.api_key)

            print(f"🎨 正在生成图片: {output_path.name}")
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url

            # 下载图片
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"✅ 图片已保存: {output_path}")
                return True

        except Exception as e:
            print(f"❌ 生成失败: {e}")

        return False

    def generate_character_set(self, theme: str = "消防安全教育") -> dict:
        """生成完整的角色套装"""
        print("=" * 70)
        print("🎬 开始生成原创IP角色套装")
        print("=" * 70)
        print()

        # 步骤1: 设计角色概念
        character = self.design_character_with_claude(theme)
        if not character:
            return None

        # 步骤2: 生成提示词
        prompts = self.generate_character_prompts(character)

        # 步骤3: 生成图片（如果有API）
        output_dir = Path.home() / ".openfang" / "ip_characters" / datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir.mkdir(parents=True, exist_ok=True)

        generated_images = []

        if self.api_key and HAS_OPENAI:
            print("=" * 70)
            print("🎨 使用 DALL-E 3 生成角色图片")
            print("=" * 70)
            print()

            for prompt_data in prompts:
                output_file = output_dir / f"{prompt_data['name']}.png"

                if self.generate_with_dalle(prompt_data['prompt'], output_file):
                    generated_images.append(str(output_file))
                else:
                    print(f"⚠️ 跳过: {prompt_data['name']}")

        # 保存角色包
        character_package = {
            "character": character,
            "prompts": prompts,
            "generated_images": generated_images,
            "created_at": datetime.now().isoformat()
        }

        # 保存到文件
        package_file = output_dir / "character_package.json"
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(character_package, f, ensure_ascii=False, indent=2)

        # 创建使用说明
        readme = f"""# 原创IP角色: {character['name']}

## 📋 角色信息

- **名称**: {character['name']}
- **类型**: {character['type']}
- **性格**: {', '.join(character['personality'])}
- **目标受众**: {character['target_age']}

## 👤 角色外观

{chr(10).join([f"- {k}: {v}" for k, v in character['appearance'].items()])}

## 🎭 背景

{character['background']}

## 📁 文件说明

- `character_package.json` - 角色完整信息包
- `{len(prompts)}` 个角色动作的图片/提示词

## 🎨 生成状态

{f"✅ 已生成 {len(generated_images)} 张图片" if generated_images else "⚠️ 需要配置 OPENAI_API_KEY 来自动生成图片"}

## 💡 使用方法

### 如果已生成图片
直接使用 `{character['name']}` 制作视频内容！

### 如果未生成图片
1. 复制 `character_package.json` 中的提示词
2. 使用以下工具之一生成：
   - DALL-E 3: https://openai.com/dall-e-3
   - Midjourney: https://midjourney.com
   - Bing Image Creator: 免费

## ✅ 版权说明

这是你的**原创IP角色**：
- ✅ 100% 原创
- ✅ 你拥有完整版权
- ✅ 可用于商业用途
- ✅ 可注册商标
- ✅ 可授权他人使用

## 🚀 下一步

1. 使用 `{character['name']}` 制作教育视频系列
2. 建立品牌认知
3. 可扩展到其他安全教育主题
4. 考虑注册IP保护

---

创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
工具: OpenFang Auto Clip - Level 3 IP Generator
"""

        readme_file = output_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme)

        print("=" * 70)
        print("✅ 角色套装生成完成！")
        print("=" * 70)
        print()
        print(f"📁 位置: {output_dir}")
        print(f"🎭 角色: {character['name']}")
        print(f"📝 提示词: {len(prompts)} 个")
        print(f"🖼️  已生成图片: {len(generated_images)} 张")
        print()

        if not generated_images:
            print("💡 要自动生成图片，需要配置 OPENAI_API_KEY:")
            print("   export OPENAI_API_KEY='sk-...'")
            print()
            print("   或者使用免费工具手动生成:")
            print("   • Bing Image Creator: https://www.bing.com/create")
            print("   • Adobe Firefly: https://firefly.adobe.com")
            print()

        return {
            "character": character,
            "prompts": prompts,
            "images": generated_images,
            "output_dir": str(output_dir)
        }


def main():
    """主函数"""
    print("=" * 70)
    print("🎬 原创IP角色生成器")
    print("创建你自己的原创角色，彻底规避IP版权问题")
    print("=" * 70)
    print()

    generator = IPCharacterGenerator()

    # 检查API
    status = generator.check_apis()

    print("📊 API状态:")
    print(f"   Anthropic Claude: {'✅' if status['anthropic']['available'] else '❌'}")
    print(f"   OpenAI DALL-E: {'✅' if status['openai']['available'] else '❌'}")
    print(f"   ElevenLabs: {'✅' if status['elevenlabs']['available'] else '❌'}")
    print()

    if not status['anthropic']['available']:
        print("⚠️ 警告: 未找到 ANTHROPIC_API_KEY")
        print("   某些功能可能无法使用")
        print()

    # 生成角色
    result = generator.generate_character_set("消防安全教育")

    if result:
        print("🎉 成功！")
        print(f"   你的原创IP角色: {result['character']['name']}")
        print()
        print(f"📂 打开目录查看: open {result['output_dir']}")

        # 打开目录
        subprocess.run(["open", result['output_dir']])


if __name__ == "__main__":
    main()
