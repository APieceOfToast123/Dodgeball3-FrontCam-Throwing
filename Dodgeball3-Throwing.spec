# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/16979/Desktop/CPS 4893 AI/Dodgeball3-FrontCam-Throwing/Program/Dodgeball3-Throwing.pyw'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/16979/Desktop/CPS 4893 AI/Dodgeball3-FrontCam-Throwing/Program/Resources/', 'Resources'), ('C:/Users/16979/Desktop/CPS 4893 AI/Dodgeball3-FrontCam-Throwing/Program/venv/Lib/site-packages/mediapipe/', 'mediapipe')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Dodgeball3-Throwing',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\16979\\Desktop\\CPS 4893 AI\\Dodgeball3-FrontCam-Throwing\\Program\\Icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Dodgeball3-Throwing',
)
