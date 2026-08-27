# Changelog

本项目所有值得注意的变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Security

- 移除已公开泄露的明文 DeepSeek API Key（deepseek_config.json），改为 example + .gitignore + 环境变量 DEEPSEEK_API_KEY 注入（2026-08-27 深度审核 R0）。

## [1.0.0] - 2026-08-27

### Added

- 首个发行版：便携源码 zip（剔除 .venv/构建产物/输出物，依赖见 README）。
- 发布面：gitee [siwpan/ollama_generator](https://gitee.com/siwpan/ollama_generator) release `v1.0.0`（AI 文本生成库 v1.0.0）。