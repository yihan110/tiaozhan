# 阮依涵_C5_repo 链接说明

> ✅ **仓库已推送。** 项目源码已提交到 `https://github.com/yihan110/tiaozhan/tree/main/C5/md-sorter`。
> 下面的注册、建库、推送步骤保留作为操作记录；`md-sorter/` 目录即该仓库内容。
> 下面是你本人需要做的最后一步：注册 → 创建空仓库 → 把本地 `md-sorter/` 整个目录 push 上去。

---

## 一句话项目说明

**md-sorter** —— 输入一个装满 Markdown 笔记的目录，输出一份按 7 个主题（课程 / 考试 / AI / 项目 / 活动 / 心情 / 读书）自动分类的 `INDEX.md` 索引 + `manifest.json` 元数据。零第三方依赖，Python 3.10+ 直接跑。

---

## 你需要本人完成的环节

1. **注册 GitHub 账号**（如果你还没有）：https://github.com/signup
2. **创建一个 public 空仓库**：
   - 右上角 `+` → `New repository`
   - Repository name 填：`md-sorter`
   - Description 填：`Markdown 笔记自动分类索引工具（输入目录 → 输出按主题分组的 INDEX.md）`
   - 选 **Public**
   - **不要**勾选 "Add a README file" / "Add .gitignore" / "Choose a license"（我们本地已经有了，勾了会冲突）
   - 点 `Create repository`
3. **把本地目录 push 上去**（下面给的是完整命令，复制粘贴即可）

---

## 完整分步推送命令（Windows PowerShell）

> 假设你已经把本提交包里的 `md-sorter/` 文件夹放在了你喜欢的位置，比如 `D:\projects\md-sorter`。
> 把下面 `yihan110` 换成你自己的用户名。

```powershell
# 1. 进入项目目录
cd D:\projects\md-sorter

# 2. 初始化 git
git init -b main

# 3. 配置你的身份（如果是第一次用 git）
git config user.name  "阮依涵"
git config user.email "你在GitHub上注册的邮箱@example.com"

# 4. 把所有文件加入暂存区
git add .

# 5. 第一次 commit
git commit -m "feat: first release v0.1.0 — md-sorter 初版"

# 6. 关联远程仓库（把 yihan110 换成你的）
git remote add origin https://github.com/yihan110/tiaozhan.git

# 7. push 上去
git push -u origin main
```

### 预期输出

- `git add .` ：没有输出（正常）
- `git commit -m ...` ：会显示类似 `58 files changed, 1234 insertions(+)`
- `git push -u origin main` ：第一次 push 会弹出 GitHub 登录窗口（用浏览器授权即可），然后看到：
  ```
  Enumerating objects: ..., done.
  ...
   * [new branch]      main -> main
  branch 'main' set up to track 'origin/main'.
  ```

### push 成功后你会拿到的链接

```
https://github.com/yihan110/tiaozhan/tree/main/C5/md-sorter
```

把这个链接填回到这里（替换上面 `yihan110`），然后按 CHALLENGE.md 第九节的模板发群里：

> "这是我的 C5 GitHub repo：https://github.com/yihan110/tiaozhan/tree/main/C5/md-sorter —— 输入一个装满 Markdown 笔记的文件夹，就能得到按主题自动分类的 INDEX.md 索引，欢迎 star、fork、提 Issue！"

---

## 可能踩的坑

| 现象 | 怎么办 |
|------|--------|
| `git push` 报 `Authentication failed` | 用浏览器弹窗授权，不要输密码；GitHub 2021 年后已经不支持账号密码 push，要用 Personal Access Token 或浏览器 OAuth |
| `error: remote origin already exists` | 跑 `git remote remove origin` 再重新 `git remote add ...` |
| push 上去后 README 在 GitHub 上显示得乱七八糟 | 检查是不是用 Windows 记事本另存过 —— 本提交包里的 .md 都是 UTF-8 无 BOM，不要用记事本改 |
| GitHub 上 `.gitignore` 没生效、把 `__pycache__` 也传上去了 | 跑一次 `git rm -r --cached .` 然后重新 `git add . && git commit -m "chore: respect gitignore"` |

---

## 本地已经验证过的事（你 push 之前不用再跑一遍）

- `D:\01python\python.exe -m pytest tests/ -v` → **13 passed in 0.08s**（详见 `tests/run_tests_log.txt`）
- `python -m md_sorter examples/sample_notes -o examples/sample_output` → 5 篇笔记正确分到 5 个主题桶（详见 `examples/run_log.txt` 和 `examples/terminal_run.png`）
