#!/bin/bash
# GitHub 仓库创建和推送脚本

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║   🚀 OpenFang Auto Clip - GitHub 发布助手                   ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 检查是否提供了GitHub用户名
if [ -z "$1" ]; then
    echo "❌ 错误：请提供你的GitHub用户名"
    echo ""
    echo "使用方法:"
    echo "  ./push_to_github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "示例:"
    echo "  ./push_to_github.sh johndoe"
    echo ""
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="openfang-auto-clip"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo "📋 配置信息："
echo "   GitHub用户名: $GITHUB_USERNAME"
echo "   仓库名称: $REPO_NAME"
echo "   仓库URL: $REPO_URL"
echo ""

# 询问是否继续
read -p "✅ 信息正确吗？继续吗？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 取消操作"
    exit 1
fi

echo ""
echo "📍 第1步：创建GitHub仓库"
echo "─────────────────────────────────────────────────────────────"
echo ""
echo "请按以下步骤操作："
echo ""
echo "1. 打开浏览器，访问："
echo "   https://github.com/new"
echo ""
echo "2. 填写仓库信息："
echo "   Repository name: $REPO_NAME"
echo "   Description: AI-powered copyright-safe video editing"
echo "   Visibility: ✅ Public"
echo "   ⚠️  不要勾选 'Add a README file' (我们已经有了)"
echo ""
echo "3. 点击 'Create repository'"
echo ""

read -p "✅ 仓库已创建？按Enter继续..."
echo ""

# 添加remote
echo "📍 第2步：连接本地仓库到GitHub"
echo "─────────────────────────────────────────────────────────────"
echo ""

git remote add origin "$REPO_URL" 2>/dev/null || {
    # 如果remote已存在，先删除
    git remote remove origin
    git remote add origin "$REPO_URL"
}

echo "✅ Remote 已添加："
git remote -v
echo ""

# 推送
echo "📍 第3步：推送代码到GitHub"
echo "─────────────────────────────────────────────────────────────"
echo ""

# 设置主分支名
git branch -M main

# 推送
echo "正在推送..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                                                               ║"
    echo "║   ✅ 成功！代码已推送到GitHub！                             ║"
    echo "║                                                               ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🔗 仓库地址："
    echo "   $REPO_URL"
    echo ""
    echo "📌 下一步："
    echo "   1. 在GitHub上创建Release（v0.2.0）"
    echo "   2. 添加topics/tags"
    echo "   3. 发布到社交媒体"
    echo ""
    echo "📖 详细步骤请查看："
    echo "   cat PUBLISH_GUIDE.md"
    echo ""
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因："
    echo "1. GitHub仓库还未创建"
    echo "2. SSH密钥未配置（需要使用HTTPS）"
    echo "3. 网络连接问题"
    echo ""
    echo "解决方法："
    echo "1. 确保已在GitHub网站创建仓库"
    echo "2. 使用GitHub CLI：gh repo create"
    echo "3. 或手动添加remote并推送"
    echo ""
fi
