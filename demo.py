# -*- coding: utf-8 -*-
"""
ollama_generator 通用版 — 集成使用示例

演示三种使用方式：
  1. 纯文本生成（适用于任何 AI 调用场景）
  2. 生成 + 中英混排自动清洗
  3. 搭配 translator.py 使用
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # 原 D:\allin 已失效

from ollama_generator import (
    # 核心生成器
    AITextGenerator,
    OllamaTextGenerator,
    GenerationConfig,
    get_generator,
    is_ai_available,
    # 混排清洗
    BaiduCleaner,
    BaiduTranslator,
    create_baidu_cleaner,
    is_mixed_cn_en,
)


# ============================================================
# 方式一：通用 AI 文本生成
# ============================================================

def demo_basic_generation():
    """任何项目都可以直接 import 使用的基础生成"""
    config = GenerationConfig(
        backend="ollama",
        model="qwen2.5",      # 换成你的模型
        temperature=0.7,
        max_tokens=200,
    )
    gen = AITextGenerator(config)

    if not gen.is_available:
        print("[跳过] Ollama 未运行")
        return

    # 带系统提示的生成
    system = "你是一个中文奇幻小说家，擅长描绘场景。使用纯中文，不要混入英文单词。"
    result = gen.generate("描述一座悬浮在云端的魔法城市", system_prompt=system)
    print(f"生成结果: {result}")

    # 多轮对话
    reply = gen.chat([
        {"role": "user", "content": "给我三个地牢名称"},
        {"role": "assistant", "content": "1. 暗影深渊\n2. 熔火之心\n3. 冰霜要塞"},
        {"role": "user", "content": "详细描述第二个"},
    ])
    print(f"对话结果: {reply}")


# ============================================================
# 方式二：Deepseek API 生成（推荐）
# ============================================================

def demo_deepseek_generation():
    """使用 Deepseek API 生成，失败时自动降级到本地 Ollama"""
    config = GenerationConfig(
        backend="deepseek",
        model="deepseek-v4-pro",  # 或 deepseek-v4-flash
        temperature=0.7,
        max_tokens=200,
        fallback_to_ollama=True,
        fallback_model="qwen2.5",
    )
    gen = AITextGenerator(config)

    print(f"[后端] {gen.config.backend}, [模型] {gen.config.model}")
    if not gen.is_available:
        print("[跳过] Deepseek API key 未配置")
        return

    system = "你是一个中文奇幻小说家，擅长描绘场景。使用纯中文，不要混入英文单词。"
    result = gen.generate("描述一座悬浮在云端的魔法城市", system_prompt=system)
    print(f"生成结果: {result}")


# ============================================================
# 方式三：生成 + 自动清洗（确保纯中文输出）
# ============================================================

def demo_generation_with_cleaning():
    """生成内容并通过清洗器确保不出现中英混排"""
    gen = OllamaTextGenerator(GenerationConfig(temperature=0.5))
    cleaner = create_baidu_cleaner()  # 自动读取 baidu_translate_config.json

    if not gen.is_available:
        print("[跳过] Ollama 未运行")
        return

    # 模拟：AI 可能生成中英混排的内容
    # 实际上大模型有时候会在中文输出中混入英文
    system = "你是一个地牢游戏叙事者，使用中文描述。"

    # 场景描述生成
    raw_description = gen.generate(
        "描述一个黑暗的地下墓穴", system_prompt=system
    )

    if raw_description:
        print(f"原始输出: {raw_description}")
        print(f"检测混排: {is_mixed_cn_en(raw_description)}")

        # 清洗：确保纯中文
        clean_description = cleaner.purify(raw_description)
        print(f"清洗结果: {clean_description}")

        # 如果翻译器不可用，自动降级为剥离英文
        if not cleaner.translator_available:
            print("(提示：配置百度翻译 API 可获得更好的清洗效果)")


# ============================================================
# 方式三：搭配 translator.py 使用
# ============================================================

def demo_with_external_translator():
    """如果你已有 translator.py，可以直接传入 BaiduTranslator 实例"""
    gen = OllamaTextGenerator()

    # 直接传入凭据（无需配置文件）
    translator = BaiduTranslator(
        app_id="你的_APP_ID",
        app_key="你的_APP_KEY",
    )
    cleaner = BaiduCleaner(translator=translator)

    # 或者从 translator.py 中导入已配置的实例
    # from translator import BaiduTranslator as ExtTranslator
    # 注意：translator.py 中的 BaiduTranslator 与这里的是同一个逻辑
    #       可以直接 new 一个：
    #       t = ExtTranslator()
    #       if t.is_configured():
    #           cleaner = BaiduCleaner(translator=t)

    if gen.is_available and cleaner.translator_available:
        raw = gen.generate("描述一个废弃的魔法塔", system_prompt="你是中文奇幻作家。")
        clean = cleaner.purify(raw)
        print(f"翻译清洗结果: {clean}")


# ============================================================
# 快捷工具：生成即清洗
# ============================================================

class CleanGenerator:
    """带自动清洗的生成器包装 —— 一行搞定生成+清洗"""
    
    def __init__(self, gen: AITextGenerator = None,
                 cleaner: BaiduCleaner = None):
        self.gen = gen or get_generator()
        self.cleaner = cleaner or create_baidu_cleaner()
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """生成并自动清洗，返回纯中文"""
        raw = self.gen.generate(prompt, system_prompt)
        if raw is None:
            # AI 不可用，使用回退文本
            return f"(AI 不可用) {prompt[:30]}..."
        return self.cleaner.purify(raw)
    
    def chat(self, messages: list) -> str:
        """对话生成并自动清洗"""
        raw = self.gen.chat(messages)
        if raw is None:
            return "(AI 不可用)"
        return self.cleaner.purify(raw)


def demo_clean_generator():
    """一行代码：生成即纯中文"""
    cg = CleanGenerator()
    
    if cg.gen.is_available:
        result = cg.generate(
            "描述一个哥布林巢穴",
            system_prompt="你是地下城游戏的叙事者，使用纯中文描述。"
        )
        print(f"一键清洗结果: {result}")
    else:
        result = cg.generate("描述一个哥布林巢穴")
        print(f"回退结果: {result}")


# ============================================================
# 配置方法
# ============================================================

HOW_TO_CONFIGURE = """
--- 百度翻译 API 配置 ---

1. 注册百度翻译开放平台: https://fanyi-api.baidu.com/
2. 获取 App ID 和 Key
3. 创建配置文件 baidu_translate_config.json:

{
    "app_id": "你的AppID",
    "app_key": "你的Key"
}

4. 将文件放在你的项目根目录，或通过参数指定路径:
   cleaner = create_baidu_cleaner(config_path="path/to/config.json")

5. 无翻译器时，自动降级为"剥离英文片段"策略（效果有限）
"""


# ============================================================
# 运行
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ollama_generator 集成示例")
    print("=" * 60)

    print("\n[方式一] 通用 AI 文本生成（Ollama）")
    demo_basic_generation()

    print("\n[方式二] Deepseek API 生成")
    demo_deepseek_generation()

    print("\n[方式三] 生成 + 中英混排自动清洗")
    demo_generation_with_cleaning()

    print("\n[方式四] 搭配 translator.py 使用")
    demo_with_external_translator()

    print("\n[快捷工具] CleanGenerator 一键清洗")
    demo_clean_generator()

    print(HOW_TO_CONFIGURE)
