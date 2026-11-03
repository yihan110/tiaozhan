# -*- coding: utf-8 -*-
"""
文枢 AI · 大学生文书与竞赛材料助手（Flask 入口）

运行：
    pip install -r requirements.txt
    python app.py
默认监听 http://127.0.0.1:5000
"""
import os
import sys

from flask import Flask, render_template, request, jsonify

from config import Config
import ai_service


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/")
def index():
    return render_template(
        "index.html",
        app_name=Config.APP_NAME,
        version=Config.APP_VERSION,
        modes=ai_service.MODES,
        has_real_ai=Config.has_real_ai(),
    )


@app.route("/api/health")
def health():
    return jsonify({
        "ok": True,
        "app": Config.APP_NAME,
        "version": Config.APP_VERSION,
        "real_ai_configured": Config.has_real_ai(),
        "model": Config.OPENAI_MODEL if Config.has_real_ai() else None,
    })


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    mode = data.get("mode", "resume")
    api_key = (data.get("api_key") or "").strip()

    if mode not in ai_service.MODES:
        return jsonify({"error": f"未知模式：{mode}"}), 400

    result = ai_service.analyze(text, mode, api_key=api_key)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    # debug=False：真实运行模式
    print(f"[启动] {Config.APP_NAME} v{Config.APP_VERSION}")
    print(f"[模式] 真实 AI 已配置：{Config.has_real_ai()}（model={Config.OPENAI_MODEL}）")
    print(f"[地址] http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
