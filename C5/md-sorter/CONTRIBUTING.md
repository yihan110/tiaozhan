# 贡献指南

很高兴你愿意给 md-sorter 提改进！本项目是一个学生练手项目，欢迎各种 PR —— 哪怕只是改个错别字。

## 本地开发

```bash
git clone https://github.com/yihan110/tiaozhan.git
cd md-sorter
pip install -r requirements.txt       # 装 pytest
$env:PYTHONPATH="src"                # Windows
# export PYTHONPATH=src               # macOS / Linux
python -m pytest tests/ -v           # 跑全部测试
```

## 提交 PR 前自查

- [ ] `python -m pytest tests/ -v` 全部通过
- [ ] 新增功能配了至少一个测试用例
- [ ] 新功能在 README 的「项目结构」或「使用」里有更新
- [ ] 在 `CHANGELOG.md` 的 `[Unreleased]` 下加了一行
- [ ] commit message 用动宾短语（如「add: 支持 .markdown 后缀」）

## 能贡献什么

- **新主题桶**：在 `src/md_sorter/classifier.py` 的 `THEME_RULES` 里加一行，记得同步加测试。
- **新文件格式**：目前只吃 `.md / .markdown`，想加 `.txt` / `.org` 欢迎提 PR。
- **性能**：目录特别大时（>1 万篇）现在是单线程，欢迎加并发扫描。
- **Bug**：直接开 Issue，附上输入目录结构和最小复现用例。

## 行为准则

友好、对事不对人。学生项目，大家都是来学习的，别上价值。
