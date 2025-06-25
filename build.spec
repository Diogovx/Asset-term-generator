# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\diogo.xavier\\Documents\\python\\termos'],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('core/*.py', '.'),
        ('config/*.yml', '.'),
        ('config/*.toml', '.'),
        ('ui/*.py', '.'),
        ('config/.env', 'config'),
        ('README.md', '.'),
        ('api/*.py', 'api'),
        ('models/*.py', 'models'),
        ('util/*.py', 'util'),
        ('logs/*.log', 'logs')
    ],
    hiddenimports=['api', 'models', 'util', 'logs'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Gerador_de_Termos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mude para False se não quiser o console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)