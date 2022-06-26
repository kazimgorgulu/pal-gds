# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../palgds/'))


# -- Project information -----------------------------------------------------

project = 'palgds'
copyright = '2022, Kazim Gorgulu'
author = 'Kazim Gorgulu'

# The full version, including alpha/beta/rc tags
release = '1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
    ]

autodoc_mock_imports = ["gdstk", "numpy", "palgds"]

autoclass_content = 'both' # selects what content will be inserted into the main body of an autoclass directive. "init", "class", "both"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates', '_tutorial']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
#html_theme = 'alabaster'
html_show_sphinx = True

pygments_style = "trac"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']



# Check below options for anything specific:

# extensions = [
#     "sphinx.ext.autodoc",
#     "sphinx.ext.napoleon",
#     "sphinx.ext.autosummary",
#     "sphinx_inline_tabs",
# ]
#
# autosummary_generate = True
# autosummary_imported_members = True
#
# napoleon_google_docstring = True
# napoleon_numpy_docstring = False
# napoleon_include_init_with_doc = False
# napoleon_include_private_with_doc = False
# napoleon_include_special_with_doc = False
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = True
# napoleon_use_admonition_for_references = False
# napoleon_use_ivar = True
# napoleon_use_param = True
# napoleon_use_rtype = True
#
# exclude_patterns = ['Thumbs.db', '.DS_Store']
#
# html_static_path = ['_static']
#
# templates_path = ["_templates"]
#
# pygments_style = "trac"
#
# html_copy_source = False
#
# html_show_sphinx = False
#
# html_theme = "sphinx_rtd_theme"
#
# html_theme_options = {
#     #'canonical_url': '',
#     #'analytics_id': '',
#     #'logo_only': False,
#     "display_version": True,
#     #'prev_next_buttons_location': 'bottom',
#     #'style_external_links': False,
#     #'vcs_pageview_mode': '',
#     "collapse_navigation": True,
#     "sticky_navigation": True,
#     "navigation_depth": -1,
#     #'includehidden': True,
#     #'titles_only': False
# }
