# -*- mode: python ; coding: utf-8 -*-
import os

# 入口脚本解析（去本地化）：
#   原硬编码绝对路径指向桌面的 ollama_generator.py，该脚本已不在仓内（git ls-files 无命中）。
#   优先级：环境变量 OLLAMA_GENERATOR_SRC → SPECPATH 同目录候选 → fail-loud 并点名变量。
_ENTRY_ENV = 'OLLAMA_GENERATOR_SRC'
_ENTRY = os.environ.get(_ENTRY_ENV) or None
if not _ENTRY:
    _cand = os.path.join(SPECPATH, 'ollama_generator.py')
    if os.path.exists(_cand):
        _ENTRY = _cand
if not _ENTRY:
    raise SystemExit(
        'ollama_generator.spec: 未找到入口脚本 ollama_generator.py（仓内不存在该文件）。\n'
        '  请设置环境变量 %s 指向入口 .py 后重试。\n'
        '  例如（临时用仓内 demo.py 打包）: set %s=%s' % (_ENTRY_ENV, _ENTRY_ENV, os.path.join(SPECPATH, 'demo.py'))
    )

a = Analysis(
    [_ENTRY],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ollama_generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
