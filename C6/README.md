# 文枢 AI · 大学生文书与竞赛材料助手

> Elite20 挑战 C6 Web Application 提交包 —— 阮依涵（郑州西亚斯学院 · 软件工程）

一个打开浏览器就能用的 AI Web App：**输入一段简历经历 / 文书 / 竞赛草稿 / 长文档 → AI 诊断打分 → 给出结构化改写建议**。
无需注册，无需登录，开箱即有「本地演示模式」；配置自己的 AI Key 后切换为真实大模型分析。

---

## 一、它解决什么问题

大学生最常写又最写不好的四类文字：

| 场景 | 痛点 | 本工具做什么 |
|---|---|---|
| 简历 / 经历 | 写得像流水账、没数据、没动词 | 四维打分 + 动词开头 / 量化数据建议 |
| 文书 / 自我介绍 | 结构散、语气平、没说服力 | 结构 / 语气 / 说服力诊断 + 改写示范 |
| 竞赛材料 | 草稿散乱、缺背景-动作-结果 | 自动抽出要点并重组为结构化条目 |
| 长文档摘要 | 报告 / 会议记录太长不想读 | 一句话摘要 + 关键要点 + 关键词 |

## 二、AI 在哪里（核心功能，不是点缀）

- 后端 `ai_service.py` 是 AI 调用层。
- **真实模式**：调用 OpenAI 兼容接口（`/chat/completions`），支持 OpenAI / DeepSeek / 通义 / Moonshot / OpenRouter 等任何兼容端点。
- **本地演示模式**（无 Key 时自动启用）：规则引擎做真实的文本分析——句子切分、中文关键词抽取、结构识别、四维加权打分、针对性建议。输出明确标注 `ai_mode = mock`，**不伪装成真实 AI**。
- 前端结果卡片上会用徽章显示当前是「真实 AI」还是「本地演示」。

## 三、输入什么 / 输出什么

- **输入**：一个模式选择 + 一段 ≤ 8000 字的中文文本（可选：在「高级」里临时填自己的 AI Key）。
- **输出**：
  - 综合分 + 四个维度分（长度 / 结构 / 简洁 / 行动数据）带进度条；
  - 抽取到的关键词；
  - 按模式定制的结构化 sections（打分卡 / 一句话摘要 / 关键要点等）；
  - 针对性改写建议列表。

## 四、怎么跑起来

```powershell
# 1. 进入 app 目录
cd app

# 2. 安装依赖
python -m pip install -r requirements.txt

# 3. （可选）配置真实 AI Key，不配置则进入本地演示模式
$env:OPENAI_API_KEY = "sk-你的key"
$env:OPENAI_BASE_URL = "https://api.openai.com/v1"   # 或其他兼容端点
$env:OPENAI_MODEL = "gpt-4o-mini"

# 4. 启动
python app.py
# 浏览器打开 http://127.0.0.1:5000
```

## 五、目录结构

```
挑战C6_阮依涵_提交包/
├── app/                       # 完整可运行的 Flask 应用
│   ├── app.py                 # Flask 入口（路由 + /api/analyze）
│   ├── ai_service.py           # AI 调用层（真实 + 本地演示）
│   ├── config.py               # 配置（全部走环境变量）
│   ├── requirements.txt
│   ├── .env.example
│   ├── templates/index.html    # 单页 UI（Tailwind CDN，响应式）
│   ├── AI_LOG.md               # 仓库内 AI 日志
│   └── ATTRIBUTION.md          # 仓库内拿来说明
├── screenshots/                # 本机真实运行截图
│   ├── 01_home.png             # 首页
│   └── 02_result.png          # 分析结果页
├── docs/
│   ├── 部署说明.md             # Vercel / 本地分步指南
│   ├── Demo录制说明.md
│   └── 提交流程说明.md
├── 阮依涵_C6_AI日志.md
├── 阮依涵_C6_拿来说明.md
├── 阮依涵_C6_AAR.md
├── 阮依涵_C6_app链接.md        # 部署后由本人填 URL
├── 阮依涵_C6_repo链接.md       # 推到 GitHub 后由本人填
└── README.md（本文件）
```

## 六、需要用户本人账号 / Key 才能完成的环节

1. **真实 AI 调用**：需要用户自己的 `OPENAI_API_KEY`（或兼容服务的 Key）。本包不附带任何 Key。
2. **公网部署 URL**：需要用户自己的 Vercel / Netlify / GitHub 账号，按 `docs/部署说明.md` 操作。
3. **GitHub repo**：需要用户自己的 GitHub 账号推送代码。
4. **Demo 视频录制**：需要用户本人在本地录屏（步骤见 `docs/Demo录制说明.md`）。

## 七、本机已验证

- `python app.py` 启动成功，监听 127.0.0.1:5050。
- `GET /api/health` 返回 `{"ok":true,"real_ai_configured":false,...}`。
- `POST /api/analyze`（mode=resume，一段真实简历文本）返回 `ai_mode=mock, overall=63~77`，三个 sections 完整。
- 用 Edge headless 真实打开页面并截图（见 `screenshots/`），首页与结果页均渲染正常。
