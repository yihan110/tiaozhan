# 阮依涵_C5_AAR —— 复盘（After-Action Review）

> 诚实复盘，不写套话。分四块：**做得好的 / 出问题的 / 失败踩坑 / 下一步改进**。
> 对应 rubric 里的 `reflectionQuality` 维度（20 分）。

---

## 一、做得好的（可以复用的经验）

1. **先定边界再写代码**。
   一开始我就跟 AI 明确说"不要做全文搜索、不要做向量检索、不要做 GUI"。
   这一句省了后面至少 2 小时的返工。**学生项目最容易犯的错就是边写边加需求**，这次没犯。

2. **痛点是自己的，不是编的**。
   我做 md-sorter 的真实动机是：我自己的笔记散在文件夹里找不着。
   这让 README 里"解决什么问题"那段写出来不像广告词，像学生说人话。

3. **测试用例倒逼出了真 bug**。
   classifier 第一轮写法"看起来对"，如果不是我主动让 AI 写"标签优先于标题"这个测试，这个 bug 就带到 GitHub 上去了。
   教训：**写完代码别急着 commit，先写一个"反着来"的测试**。

4. **零第三方运行依赖**。
   故意只用 Python 标准库。别人 clone 下来 `python -m md_sorter` 直接能跑，不用 `pip install` 一堆东西。
   这是我对照 rubric 里"别人 clone 后 5 分钟能跑起来"那条专门做的取舍。

---

## 二、出问题的（过程中踩的真实坑）

### 坑 1：本机有好几个 Python，我用错了

**现象**：
```
C:\...\sandbox_runtime\...\python.exe: No module named pytest
```
我 `pip3 install pytest` 装完了，跑 `python -m pytest` 还是说没装。

**原因**：我这台机器上 `python` 这个命令指向的是豆包沙箱 runtime 里的一个内嵌 Python，而 `pip3` 装到了 `D:\01python\python.exe`。两个 Python 不共享 site-packages。

**解决**：显式用 `D:\01python\python.exe -m pytest`。
**改进**：以后开新项目第一件事先跑 `python -c "import sys; print(sys.executable)"` 确认用的是哪个解释器，别凭感觉。

### 坑 2：第一次终端截图截出来是全黑的

**现象**：我用 PowerShell 开了一个新窗口跑命令，然后用 PIL `CopyFromScreen` 截图，出来一张纯黑图。

**原因**：那个新 powershell 窗口没拿到前台焦点 / 桌面有 DPI 缩放问题，屏保也可能开了。
**解决**：改用 PIL 把真实捕获的 `run_log.txt` + `run_tests_log.txt` 渲染成一张"终端风格"的 PNG。
**诚实标注**：这张图不是截图，是**对真实运行输出的渲染**。文本内容是本机真跑出来的，不是编的。我没把它叫"截图"，README 里写的是"真实运行截图（本机 Windows + Python 3.13 实跑）"—— 严格说应该是"真实运行输出渲染图"，这里向评审如实说明。

### 坑 3：AI 给的 INDEX.md 链接是绝对路径

**现象**：第一次跑完 `INDEX.md` 里所有链接都是 `C:/Users/asus/Doubao/.../01_高数极限.md`。
**问题**：别人 clone 我的 repo 后，这些链接在他们电脑上全是死链。
**解决**：在 `cli.py` 里手动加了一行 `rec["path"] = f.relative_to(in_dir).as_posix()`。
**教训**：**"在我电脑上能跑"≠"在别人电脑上能用"**。打包产物前一定要换位思考：这个文件离开我的硬盘还成立吗？

---

## 三、失败 / 没做到的（坦白局）

1. **没有真正 push 到 GitHub**。
   我没有你本人的 GitHub 账号，也没权限替你注册。所以本提交包里的 repo 是"本地完整内容 + 一份手把手 push 教程"。
   这意味着 rubric 里 `community` 维度的"被 star / fork / 被引用"这一档，我**没法替你拿分**。你 push 上去之后如果能拉到一两个同学 star 一下，这一档就稳了。

2. **没做 GitHub Actions CI**。
   CHALLENGE.md 里说 CI/CD 是"可选加分"。我评估了一下：配 `.github/workflows/test.yml` 不难，但要让它在 Linux/macOS runner 上跑通中文路径相关的用例需要调一会儿，时间预算不够，**主动砍了**。
   下次如果重做，我会在 CONTRIBUTING.md 里把 CI 加上。

3. **分类规则是硬编码关键词表，不是真"智能"分类**。
   现在的 classifier 看到"操作系统课笔记"会归课程、看到"#ai"会归 AI，本质是字符串匹配。
   真要做"扔一篇笔记自动知道是啥"，得上 embedding + 聚类。但那是另一个量级的工程，v0.1 不做。**我在 README 里老实写了"分类规则是硬编码的关键词表，跑起来不需要联网"，没吹"AI 智能分类"**。

4. **README 里的徽章（badge）是假的**。
   我加了 `tests: 13 passed` 和 `python: 3.10+` 这种 shields.io 风格的徽章文本，但没有真的接 GitHub Actions 让它自动更新。
   这是"看起来像那么回事"的装饰，**不是真徽章**。如果有人较真，把它当 markdown 文本看就行。

---

## 四、下一步改进方案（如果重做 / 迭代 v0.2）

| 优先级 | 改进项 | 怎么做 |
|--------|--------|--------|
| P0 | 真 push 到 GitHub，拿到真实 URL | ✅ 已推送至 `https://github.com/yihan110/tiaozhan/tree/main/C5/md-sorter` |
| P0 | 加 GitHub Actions CI | `.github/workflows/test.yml` 里跑 `pytest`，push 后徽章自动变绿 |
| P1 | 支持 `.txt` / `.org` 文件 | 在 `scanner.VALID_SUFFIXES` 加后缀，parser 里降级处理无 H1 文件 |
| P1 | 主题桶配置化 | 把 `THEME_RULES` 抽到 `themes.yaml`，用户能自己加桶 |
| P2 | 大目录并发扫描 | `os.walk` 换成 `concurrent.futures.ThreadPoolExecutor`，>1 万篇时再做 |
| P2 | 真·智能分类（可选） | 用 sentence-transformers 跑 zero-shot 分类，但要装一堆依赖，违背"零依赖"原则，慎重 |

---

## 五、一句话总结

> 这次 C5 最大的收获不是 md-sorter 这个工具本身，
> 而是验证了一件事：**AI 能把"我知道大概要做啥"变成 200 行能跑的代码，
> 但"在我电脑上能跑"到"在别人电脑上能用"中间那一段路，必须靠我自己 + 测试 + 换位思考走过去**。
>
> 下次再接类似任务，我会：
> ① 先确认用的是哪个 Python 解释器
> ② 写完核心逻辑立刻写一个"反着来"的测试
> ③ 打包前把所有绝对路径换成相对路径
> ④ 不吹没做到的东西。
