# Ollama Generator — AI 文本生成库

> 仓库：<https://gitee.com/siwpan/ollama_generator> ｜ 许可：MIT（见 [LICENSE](LICENSE)）

基于 Ollama 的通用 AI 文本生成库，支持多轮对话和中文清洗。

## 功能

- **多轮对话** — 通用 AI 文本生成，可配置系统提示词
- **中英混排清洗** — 自动检测中英混排文本，通过百度翻译 API 或英文剥离策略清洗
- **游戏场景提示词** — 内置房间描述 / 怪物 / 战斗 / 故事等游戏专用提示词
- **可复用设计** — 标准 Python 包，`from ollama_generator import ...` 即可使用

## 快速开始

```bash
# 安装 Ollama (可选)
# https://ollama.com/

# 安装依赖
pip install ollama

# 运行演示
python demo.py
```

## 使用示例

```python
from ollama_generator import OllamaTextGenerator, BaiduCleaner

# 文本生成
gen = OllamaTextGenerator(model="qwen2.5:7b")
result = gen.generate("描述一个黑暗森林")

# 中文清洗
cleaner = BaiduCleaner(api_key="your_key", secret="your_secret")
clean_text = cleaner.clean("I think this is 非常好的 idea")
```

## 项目结构

```
ollama_generator/
├── __init__.py           # 包导出
├── core.py               # 核心生成器
├── cleaner.py            # 中英混排清洗
├── demo.py               # 四种使用方式演示
└── ollama_generator.py   # 旧版兼容入口
```

## 依赖

- Python >= 3.8
- ollama (可选)
- 百度翻译 API (可选，用于中文清洗)
