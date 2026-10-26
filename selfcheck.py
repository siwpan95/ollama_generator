# -*- coding: utf-8 -*-
"""无头自检（不连 AI 服务）：包可导入 + 配置默认值 + 中英混排判定 + 清洗器构造。

用法：python selfcheck.py    （退出 0 = 通过）
生成器的在线调用需要 Ollama/DeepSeek，不在无头自检范围内。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))

import ollama_generator as og  # noqa: E402


def main() -> int:
    config = og.GenerationConfig()
    if not getattr(config, "model", ""):
        print("FAIL GenerationConfig has no default model")
        return 1

    cases = {"hello 世界": True, "pure english text": False, "纯中文": False}
    for text, expected in cases.items():
        got = og.is_mixed_cn_en(text)
        if got is not expected:
            print(f"FAIL is_mixed_cn_en({text!r}) -> {got}, expected {expected}")
            return 1

    cleaner = og.create_baidu_cleaner()
    if cleaner is None:
        print("FAIL create_baidu_cleaner returned None")
        return 1

    # 离线可用性探测只要求返回布尔值，不要求真的连上服务
    if not isinstance(og.is_ai_available(), bool):
        print("FAIL is_ai_available did not return bool")
        return 1

    print("ollama_generator selfcheck ok: import / config / mixed-detection / cleaner")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
