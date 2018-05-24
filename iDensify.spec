# -*- mode: python -*-

block_cipher = None

a = Analysis(['iDensify.py'],
             pathex=['./'],
             binaries=[],
             datas=[('./header.png', '.')],
             hiddenimports=None,
             hookspath=[],
             runtime_hooks=None,
             excludes=None,
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='iDensify',
          debug=True,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=False , icon='icon.icns')

app = BUNDLE(exe,
             name='iDensify.app',
             icon='/Users/hkdb/AeroFS/Private/Development/iDensify/icon.icns',
             bundle_identifier='com.3df.osx.idensify',
             info_plist={
               'CFBundleName': 'iDensify',
               'CFBundleDisplayName': 'iDensify',
               'CFBundleGetInfoString': 'PDF Compressor',
               'CFBundleIdentifier': 'com.3df.osx.idensify',
               'CFBundleVersion': '0.1.0',
               'CFBundleShortVersionString': '0.1.0',
               'NSHumanReadableCopyright': '3DF OSI - MIT License'
              }
             )
