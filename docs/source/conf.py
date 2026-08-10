# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Package lives at src/siesta -- this makes `import siesta` work even when
# building docs from an environment that doesn't have siesta-rest-editor pip
# installed (editable or otherwise).
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

project = "siesta-rest-editor"
copyright = "2025, Shavin Kaluthantri, Derrick Hasterok, and Maggie Li"
author = "Shavin Kaluthantri, Derrick Hasterok, and Maggie Li"
release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "numpydoc",
]

autosummary_generate = True
autosummary_imported_members = False
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/__pycache__/**", "**/.venv/**", "**/venv/**"]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "inherited-members": False,
    "show-inheritance": True,
}
autoclass_content = "both"

# see lame-core's docs/source/conf.py (and LaME's) for why this matters:
# without it, numpydoc's per-class "Methods" table tries to link every
# inherited PyQt6 method to an autosummary stub page that never gets
# generated, producing thousands of spurious "stub file not found" warnings.
numpydoc_class_members_toctree = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "docutils": ("https://docutils.sourceforge.io/docs/", None),
    # local sibling repo, checked out alongside this one (../../../lame-core) --
    # relative path so it stays valid regardless of the absolute checkout
    # location, as long as the sibling repos stay siblings. Requires lame-core's
    # own docs to have been built first (its docs/build/html/objects.inv).
    "lame_core": ("../../../lame-core/docs/build/html", None),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/dhasterok/siesta-rest-editor",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
}