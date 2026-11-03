# 阮依涵 C6 拿来说明（ATTRIBUTION）

> 本项目哪些地方参考了别人、参考了什么、我改了哪里。诚实列出，不藏。

---

## 1. 设计参考

| 参考对象 | 参考了什么 | 我改了哪里 |
|---|---|---|
| Tailwind UI 官方组件示例（card / tab / progress bar） | 圆角卡片、tab 切换、进度条的视觉样式 | 没有用 React 版，改成纯 HTML + Tailwind CDN；配色从默认 indigo 改成本产品的 indigo→purple 渐变 |
| 内置 `html` 技能（Doubao 工作区） | 单页 Web 应用的整体结构约定：一个 index.html、内联少量 CSS、原生 JS | 没有用它的模板内容，只借了"单文件 + CDN 依赖"这种最轻量的组织方式 |
| OpenAI 官方 Cookbook（chat/completions 调用示例） | `POST {base_url}/chat/completions`、`messages` 数组、`Authorization: Bearer` 头的写法 | 改成可配置 `OPENAI_BASE_URL`，兼容 DeepSeek / 通义 / Moonshot / OpenRouter；加了 `requests` 异常捕获和超时 |

## 2. 代码来源

| 模块 | 来源 | 改动 |
|---|---|---|
| Flask 路由骨架（`/`、`/api/health`、`POST /api/analyze`） | AI 生成（prompt 见 AI 日志阶段 2） | 加了 mode 白名单校验、8000 字上限、`api_key` 可选参数 |
| 中文分词/关键词抽取正则 `[一-龥]{2,4}` | AI 生成 | 加了停用词表、包含关系去重（"无人机" vs "机社团"） |
| 四维打分规则 | AI 给出初版权重 | 我自己调过：长度 0.25 / 结构 0.25 / 简洁 0.2 / 行动数据 0.3，因为对简历场景"动词+数据"最关键 |
| 前端 fetch 调用 | AI 生成 | 加了 `?demo=1` 自动演示参数、结果去重 |

## 3. 没有用到的东西（诚实声明）

- **没有** fork 任何 GitHub repo。
- **没有** 用 shadcn/ui / Chakra UI / React 组件库——为了部署简单。
- **没有** 用 v0.dev / Bolt / Lovable 等低代码平台生成完整产物。
- **没有** 把任何真实 API Key 写进代码——所有 Key 都走环境变量或前端临时输入。

## 4. 素材

- 截图：Edge headless 真实打开本地 `http://127.0.0.1:5050/` 截取，非设计稿。
- 样例文本：用的是我自己的真实简历片段（无人机社团副社长、华为 ICT 省级三等奖），不是网上抄的。
