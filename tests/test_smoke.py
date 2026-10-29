# -*- coding: utf-8 -*-
"""ollama_generator 最小测试骨架（离线冒烟，纯逻辑，不联网、不装模型）。

运行：
    python -m unittest discover -s tests -v        （仓库根目录）
或：
    python -m unittest tests.test_smoke -v

覆盖：包 API 面 + cleaner 纯函数（中英混排判定 / 英文片段剥离）。
"""
import os
import sys
import unittest

# 扁平包布局（__init__.py 在仓库根）：把仓库根的父目录放入 sys.path，
# 使 `import ollama_generator` 可从任意运行器解析。
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(_REPO_ROOT))


class TestPackageApi(unittest.TestCase):
    def test_api_surface(self):
        import ollama_generator
        for name in ("OllamaTextGenerator", "get_generator", "is_ai_available",
                     "BaiduCleaner", "create_baidu_cleaner"):
            self.assertTrue(hasattr(ollama_generator, name),
                            f"missing export: {name}")


class TestCleanerPure(unittest.TestCase):
    def test_counters(self):
        from ollama_generator.cleaner import count_chinese_chars, count_english_words
        self.assertEqual(count_chinese_chars("你好，世界"), 4)
        self.assertEqual(count_english_words("hello brave new world"), 4)
        self.assertEqual(count_chinese_chars("pure english"), 0)
        self.assertEqual(count_english_words("纯中文"), 0)

    def test_is_mixed(self):
        from ollama_generator.cleaner import is_mixed_cn_en
        self.assertTrue(is_mixed_cn_en("这是一段中文 test mixed 混排文本"))
        self.assertFalse(is_mixed_cn_en("纯中文没有英文"))
        self.assertFalse(is_mixed_cn_en("only english here"))
        self.assertFalse(is_mixed_cn_en("   "))

    def test_strip_english_fragments(self):
        from ollama_generator.cleaner import strip_english_fragments
        out = strip_english_fragments("这是一句中文 This is an english fragment 结束。")
        self.assertNotIn("fragment", out)
        self.assertIn("结束", out)
        # 纯中文输入应基本原样保留
        self.assertIn("纯中文", strip_english_fragments("纯中文，标点。"))


if __name__ == "__main__":
    unittest.main()
