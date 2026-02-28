#!/usr/bin/env python3
"""
OpenFang Auto Clip - Web管理界面
本地Web服务器，提供可视化操作界面
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
import subprocess
import json
import os
from pathlib import Path
import threading
import time
from datetime import datetime

app = Flask(__name__)

# 配置
PROJECT_DIR = Path("/Users/terre/Desktop/openfang-auto-clip")
OUTPUT_DIR = Path.home() / ".openfang"
IP_CHARACTERS_DIR = OUTPUT_DIR / "ip_characters"

# 存储运行状态
task_status = {}


def run_command_async(command, task_id):
    """异步运行命令"""
    try:
        task_status[task_id] = {
            'status': 'running',
            'output': '',
            'error': '',
            'start_time': datetime.now().isoformat()
        }

        process = subprocess.Popen(
            command,
            shell=True,
            cwd=str(PROJECT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        stdout, stderr = process.communicate()

        task_status[task_id].update({
            'status': 'completed' if process.returncode == 0 else 'error',
            'output': stdout,
            'error': stderr,
            'end_time': datetime.now().isoformat()
        })

    except Exception as e:
        task_status[task_id].update({
            'status': 'error',
            'error': str(e),
            'end_time': datetime.now().isoformat()
        })


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
        'python_version': os.popen('python3 --version').read().strip(),
        'tasks': task_status
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
            if char_dir.is_dir() and char_dir.name.startswith('level3_project_') or char_dir.name.startswith('20260228_'):
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
    task_id = f"ip_char_{int(time.time())}"

    # 在后台运行
    thread = threading.Thread(
        target=run_command_async,
        args=(f"cd {PROJECT_DIR} && python3 generate_ip_character.py", task_id)
    )
    thread.start()

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
    task_id = f"transform_{int(time.time())}"

    thread = threading.Thread(
        target=run_command_async,
        args=(f"cd {PROJECT_DIR} && python3 test_transform.py", task_id)
    )
    thread.start()

    return jsonify({
        'task_id': task_id,
        'message': '版权转换任务已启动'
    })


@app.route('/api/create-clips', methods=['POST'])
def create_clips():
    """创建视频片段"""
    task_id = f"clips_{int(time.time())}"

    thread = threading.Thread(
        target=run_command_async,
        args=(f"cd {PROJECT_DIR} && python3 test_clips.py", task_id)
    )
    thread.start()

    return jsonify({
        'task_id': task_id,
        'message': '视频片段创建任务已启动'
    })


@app.route('/api/level3-recreate', methods=['POST'])
def level3_recreate():
    """Level 3 完全重制"""
    task_id = f"recreate_{int(time.time())}"

    thread = threading.Thread(
        target=run_command_async,
        args=(f"cd {PROJECT_DIR} && python3 level3_recreator.py", task_id)
    )
    thread.start()

    return jsonify({
        'task_id': task_id,
        'message': 'Level 3 完全重制任务已启动'
    })


@app.route('/api/task-status/<task_id>')
def get_task_status(task_id):
    """获取任务状态"""
    if task_id in task_status:
        return jsonify(task_status[task_id])
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/api/open-directory')
def open_directory(path=None):
    """打开目录"""
    try:
        dir_path = path or OUTPUT_DIR
        subprocess.run(['open', dir_path])
        return jsonify({'message': f'已打开目录: {dir_path}'})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/process-video', methods=['POST'])
def process_video():
    """处理YouTube视频"""
    data = request.json
    url = data.get('url', '')
    transform_level = data.get('transform_level', 1)

    if not url:
        return jsonify({'error': '请提供视频URL'}), 400

    task_id = f"video_{int(time.time())}"
    command = f"cd {PROJECT_DIR} && python3 auto_clip.py \"{url}\" --transform {transform_level}"

    thread = threading.Thread(
        target=run_command_async,
        args=(command, task_id)
    )
    thread.start()

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
