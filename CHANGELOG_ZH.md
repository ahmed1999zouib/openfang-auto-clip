# 更新日志

本文档记录 OpenFang Auto Clip 的主要版本变化。

格式参考 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)，版本遵循语义化版本管理。

## [未发布]

### 已新增
- GitHub Actions CI
- 开发依赖清单 `requirements-dev.txt`
- 安装说明 `docs/INSTALLATION.md`
- Benchmark demo、storyboard 输出和 launch kit 生成器
- `release_prep.py` 与 tag release 自动化
- 中英双语 landing page 和文档索引

### 已调整
- 安装脚本与运行时统一使用 `~/.openfang`
- Web 管理器改为更安全、可迁移、可持久化的执行模型
- README、发布链路和 benchmark 入口统一到真实可运行命令

## [0.2.0] - 2026-02-28

### 新增
- 版权安全转换框架
- Level 1 视觉混音
- 多平台导出支持
- 自动化视频下载与 FFmpeg 处理
- 配置系统、示例配置、双语 README

### 改进
- 文件名清理
- 错误处理
- 日志输出

### 修复
- 特殊字符文件名问题
- FFmpeg 路径解析问题
- 部分下载失败场景

## [0.1.0] - 2026-02-27

### 新增
- 初始版本
- 基础视频下载
- 简单高光片段切分
- Whisper 与 OpenFang 集成框架
