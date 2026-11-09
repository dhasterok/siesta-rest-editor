"""PyInstaller runtime hook: make rst2pdf find its bundled data files.

When ``sys.frozen`` is set, rst2pdf assumes a py2exe-style layout and looks for
its ``styles/``, ``templates/`` and ``images/`` folders next to the executable
(``Contents/MacOS`` in a .app). PyInstaller puts them in the package directory
instead, which is exactly where rst2pdf looks when it is *not* frozen. So hide
``sys.frozen`` while an ``RstToPdf`` is constructed -- that is where it records
``self.PATH`` and loads the default stylesheets -- and point the module-level
"missing image" placeholder at the package directory too.
"""
import functools
import os
import sys

import rst2pdf.createpdf
import rst2pdf.image

_PKG_DIR = os.path.dirname(os.path.abspath(rst2pdf.createpdf.__file__))

rst2pdf.image.PATH = _PKG_DIR
rst2pdf.image.missing = os.path.join(_PKG_DIR, "images", "image-missing.jpg")

_orig_init = rst2pdf.createpdf.RstToPdf.__init__


@functools.wraps(_orig_init)
def _init_with_package_paths(self, *args, **kwargs):
    frozen = sys.__dict__.pop("frozen", None)
    try:
        _orig_init(self, *args, **kwargs)
    finally:
        if frozen is not None:
            sys.frozen = frozen


rst2pdf.createpdf.RstToPdf.__init__ = _init_with_package_paths
