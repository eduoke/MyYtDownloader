# -*- mode: python ; coding: utf-8 -*-


black_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Assets folder
        ('assets', 'assets'),
        # ttkbootstrap theme file
        ('themes', 'themes')
    ],
    hiddenimports=[
        'pytube',
        'ttkbootstrap',
        'controllers',
        'models',
        'views',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'threading',
        'typing',
        're',
        'os'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=black_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MyYtDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/logo_A8Y_icon.ico',
)
