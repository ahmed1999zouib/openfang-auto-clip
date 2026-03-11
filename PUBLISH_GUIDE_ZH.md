# GitHub 发布指南

这份指南用于把 OpenFang Auto Clip 的版本发布流程标准化。

## 快速路径

先生成 release bundle：

```bash
python3 scripts/release_prep.py v0.3.0 --allow-dirty
```

如果已经有 benchmark report，再生成 launch 文案：

```bash
python3 scripts/generate_launch_kit.py \
  --report examples/benchmark/sample_benchmark_report.json
```

## 推荐发布步骤

1. 运行测试
   - `python3 -m unittest discover -s tests`
2. 更新 `CHANGELOG.md`
3. 生成 release notes
4. 创建 tag
   - `git tag v0.3.0`
5. 推送主分支和 tag
   - `git push origin main`
   - `git push origin v0.3.0`

## 推送 tag 后会发生什么

`.github/workflows/release.yml` 会：

- 安装依赖
- 运行测试
- 生成 release notes
- 创建 GitHub Release

## 建议一并准备的素材

- storyboard 图片
- benchmark report
- launch kit 文案
- README 中对应的功能边界说明
