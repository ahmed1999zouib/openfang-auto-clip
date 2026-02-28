#!/bin/bash
# Web管理界面启动脚本

echo "=================================="
echo "🚀 OpenFang Auto Clip - Web管理"
echo "=================================="
echo ""

# 激活虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境并安装Flask..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask
else
    echo "✅ 使用现有虚拟环境"
    source venv/bin/activate
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
python web_manager.py
