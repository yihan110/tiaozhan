# -*- coding: utf-8 -*-
"""
配置模块：所有敏感信息均从环境变量读取，绝不硬编码。
真实 AI 调用需要用户自己配置 OPENAI_API_KEY（或兼容接口的 Key）。
未配置时，应用自动进入「本地演示模式」（规则引擎），界面会明确标注。
"""
import os


class Config:
    # ---- Flask ----
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    JSON_AS_ASCII = False

    # ---- OpenAI 兼容接口（也可接入 DeepSeek / 通义 / Moonshot / OpenRouter 等）----
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
    OPENAI_BASE_URL = os.environ.get(
        "OPENAI_BASE_URL",
        os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
    ).strip()
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini").strip()
    OPENAI_TIMEOUT = int(os.environ.get("OPENAI_TIMEOUT", "60"))

    # ---- 应用元信息 ----
    APP_NAME = "文枢 AI · 大学生文书与竞赛材料助手"
    APP_VERSION = "1.0.0"

    @classmethod
    def has_real_ai(cls):
        """是否配置了真实 AI Key。"""
        return bool(cls.OPENAI_API_KEY)
