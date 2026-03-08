#!/usr/bin/env python3
"""OpenFang Auto Clip local web manager."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.web_runtime import (
    TaskStore,
    build_python_command,
    is_allowed_path,
    parse_transform_level,
    resolve_ip_characters_dir,
    resolve_output_dir,
    resolve_project_dir,
    start_background_task,
    validate_video_url,
)

app = Flask(__name__)

PROJECT_DIR = resolve_project_dir()
OUTPUT_DIR = resolve_output_dir()
IP_CHARACTERS_DIR = resolve_ip_characters_dir()
TASK_STORE = TaskStore()


@app.route('/')
def index():
    """主页"""
    return render_template('manager.html')


@app.route('/api/status')
def get_status():
    """获取系统状态"""
    status = {
        'project_dir': str(PROJECT_DIR),
        'output_dir': str(OUTPUT_DIR),
        'python_version': sys.version.split()[0],
        'tasks': TASK_STORE.all()
    }
    return jsonify(status)


@app.route('/api/ip-characters')
def list_ip_characters():
    """列出IP角色"""
    try:
        if not IP_CHARACTERS_DIR.exists():
            return jsonify({'characters': []})

        characters = []
        for char_dir in IP_CHARACTERS_DIR.iterdir():
            if char_dir.is_dir():
                char_info = {
                    'name': char_dir.name,
                    'path': str(char_dir),
                    'modified': datetime.fromtimestamp(char_dir.stat().st_mtime).isoformat()
                }
                characters.append(char_info)

        return jsonify({'characters': sorted(characters, key=lambda x: x['modified'], reverse=True)})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/generate-ip-character', methods=['POST'])
def generate_ip_character():
    """生成IP角色"""
    task_id = start_background_task(
        "ip_char",
        build_python_command("generate_ip_character.py"),
        TASK_STORE,
        metadata={"kind": "generate_ip_character"},
        cwd=PROJECT_DIR,
    )

    return jsonify({
        'task_id': task_id,
        'message': 'IP角色生成任务已启动'
    })


@app.route('/api/open-test-page')
def open_test_page():
    """打开测试页面"""
    try:
        test_page = IP_CHARACTERS_DIR / "test.html"
        if not test_page.exists():
            # 创建测试页面
            return jsonify({'error': '测试页面不存在，请先生成IP角色'})

        subprocess.run(['open', str(test_page)])
        return jsonify({'message': '测试页面已在浏览器中打开'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/transform-video', methods=['POST'])
def transform_video():
    """测试版权转换"""
    task_id = start_background_task(
        "transform",
        build_python_command("test_transform.py"),
        TASK_STORE,
        metadata={"kind": "transform_video"},
        cwd=PROJECT_DIR,
    )

    return jsonify({
        'task_id': task_id,
        'message': '版权转换任务已启动'
    })


@app.route('/api/create-clips', methods=['POST'])
def create_clips():
    """创建视频片段"""
    task_id = start_background_task(
        "clips",
        build_python_command("test_clips.py"),
        TASK_STORE,
        metadata={"kind": "create_clips"},
        cwd=PROJECT_DIR,
    )

    return jsonify({
        'task_id': task_id,
        'message': '视频片段创建任务已启动'
    })


@app.route('/api/level3-recreate', methods=['POST'])
def level3_recreate():
    """Level 3 完全重制"""
    task_id = start_background_task(
        "recreate",
        build_python_command("level3_recreator.py"),
        TASK_STORE,
        metadata={"kind": "level3_recreate"},
        cwd=PROJECT_DIR,
    )

    return jsonify({
        'task_id': task_id,
        'message': 'Level 3 完全重制任务已启动'
    })


@app.route('/api/task-status/<task_id>')
def get_task_status(task_id):
    """获取任务状态"""
    task = TASK_STORE.get(task_id)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)


@app.route('/api/open-directory')
def open_directory():
    """打开目录"""
    try:
        requested_path = request.args.get('path')
        dir_path = Path(requested_path).expanduser() if requested_path else OUTPUT_DIR
        if not is_allowed_path(dir_path):
            return jsonify({'error': '不允许打开该目录'}), 400

        subprocess.run(['open', str(dir_path)], check=False)
        return jsonify({'message': f'已打开目录: {dir_path}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """处理YouTube视频"""
    data = request.get_json(silent=True) or {}
    url = str(data.get('url', '')).strip()

    if not url:
        return jsonify({'error': '请提供视频URL'}), 400
    if not validate_video_url(url):
        return jsonify({'error': '请输入有效的 http(s) 视频URL'}), 400

    try:
        transform_level = parse_transform_level(data.get('transform_level', 1))
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

    task_id = start_background_task(
        "video",
        build_python_command("auto_clip.py", url, "--transform", transform_level),
        TASK_STORE,
        metadata={
            "kind": "process_video",
            "url": url,
            "transform_level": transform_level,
        },
        cwd=PROJECT_DIR,
    )

    return jsonify({
        'task_id': task_id,
        'message': f'视频处理任务已启动'
    })


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 OpenFang Auto Clip - Web管理界面")
    print("=" * 70)
    print()
    print("📱 启动本地服务器...")
    print("🌐 管理界面: http://localhost:5000")
    print()
    print("💡 使用说明：")
    print("   1. 浏览器会自动打开管理界面")
    print("   2. 点击按钮即可完成各种操作")
    print("   3. 查看实时日志和任务状态")
    print()
    print("按 Ctrl+C 停止服务器")
    print("=" * 70)
    print()

    # 自动打开浏览器
    import webbrowser
    webbrowser.open('http://localhost:5000')

    # 启动服务器
    app.run(host='127.0.0.1', port=5000, debug=False)
