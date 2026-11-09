# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for building reST Editor as a standalone macOS .app.

Build with ``./build_mac.sh`` (or ``pyinstaller --noconfirm reSTEdit.spec`` from
the project's virtualenv). The result is ``dist/reST Editor.app``.

Built as a onedir bundle (not onefile): QtWebEngine, used for the HTML preview,
does not work from a onefile build on macOS.
"""
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

APP_NAME = "reST Editor"
BUNDLE_ID = "org.siesta.rest-editor"
VERSION = "0.1.0"

datas = []
hiddenimports = []

# siesta: PDF stylesheet, HTML preview CSS, print icons
datas += collect_data_files("siesta", includes=["*.css", "*.yaml", "icons/*.svg"])

# lame_core: shared toolbar icons and Qt stylesheets
datas += collect_data_files("lame_core", includes=["resources/**/*"])

# rst2pdf: default styles, templates and images are read from its package dir at
# runtime, and its directives/roles/extensions are imported by name.
datas += collect_data_files("rst2pdf")
datas += copy_metadata("rst2pdf")
hiddenimports += collect_submodules("rst2pdf")

# docutils: writers/parsers/languages are imported by name; the HTML writer
# needs html4css1.css and its template from the package dir.
datas += collect_data_files("docutils")
hiddenimports += collect_submodules("docutils")

# reportlab ships its own fonts (used by rst2pdf)
datas += collect_data_files("reportlab")

# pygments lexers/styles are looked up by name for code-block highlighting
hiddenimports += collect_submodules("pygments")

icon_file = "build/icon/reSTEdit.icns"
icon = icon_file if os.path.exists(icon_file) else None

a = Analysis(
    ["reSTEdit.py"],
    pathex=["src"],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["packaging/rthook_rst2pdf.py"],
    # Not used by the editor; keeps the bundle from ballooning if they happen
    # to be installed in the build environment.
    excludes=["tkinter", "matplotlib", "IPython", "jupyter", "notebook", "sphinx", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=False,
    target_arch=None,  # build for the architecture of the Python running PyInstaller
    codesign_identity=None,
    entitlements_file=None,
    icon=icon,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name=APP_NAME,
)

app = BUNDLE(
    coll,
    name=f"{APP_NAME}.app",
    icon=icon,
    bundle_identifier=BUNDLE_ID,
    version=VERSION,
    info_plist={
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        "NSHighResolutionCapable": True,
        "NSRequiresAquaSystemAppearance": False,  # follow system light/dark mode
        "LSApplicationCategoryType": "public.app-category.productivity",
    },
)
