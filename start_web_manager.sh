#!/bin/bash
set -euo pipefail

# Web管理界面启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================="
echo "🚀 OpenFang Auto Clip - Web管理"
echo "=================================="
echo ""

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境并安装依赖..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ 使用现有虚拟环境"
    source venv/bin/activate
    pip install -r requirements.txt >/dev/null
fi

echo ""
echo "🌐 启动Web管理界面..."
echo ""
echo "管理界面会在浏览器中自动打开"
echo "按 Ctrl+C 停止服务器"
echo ""
echo "=================================="
echo ""

# 启动Web服务器
python3 web_manager.py
