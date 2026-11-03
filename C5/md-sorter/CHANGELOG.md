# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 风格。

## [0.1.0] - 2026-11-01

### Added
- 首次发布。
- `scanner.py`：递归扫描目录，跳过 `.git` / `.venv` / `__pycache__` 等黑名单目录。
- `parser.py`：解析 Markdown 一级标题，抽取 `#标签`，对编码错误文件做降级处理不崩溃。
- `classifier.py`：内置 7 个主题桶（课程笔记 / 作业与考试 / AI 与工具 / 项目与代码 / 活动与实践 / 生活与心情 / 读书笔记），标签命中优先于标题命中。
- `indexer.py`：生成 `INDEX.md`（按主题分组的 Markdown 索引）+ `manifest.json`（结构化元数据）。
- `cli.py`：`python -m md_sorter <input_dir> -o <output_dir>` 命令行入口。
- 13 个 pytest 用例，全部通过（见 `tests/run_tests_log.txt`）。
- `examples/sample_notes/`：5 篇贴近真实学生场景的示例笔记。
