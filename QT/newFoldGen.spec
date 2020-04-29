# -*- mode: python -*-

block_cipher = None


a = Analysis(['newFoldGen.py'],
             pathex=['C:\\Users\\TZK\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'G:\\onedrive\\py\\study_dir\\QT'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='newFoldGen',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
