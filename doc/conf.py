# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import re
import os
import sys
import logging

logger = logging.getLogger(__file__)


RE_VERSION = re.compile(r'^__version__ \= \'(\d+\.\d+\.\d+(?:-\w+)?)\'$', re.MULTILINE)
PROJECTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECTDIR)


def get_release():
    with open(os.path.join(PROJECTDIR, 'coax', '__init__.py')) as f:
        version = re.search(RE_VERSION, f.read())
    assert version is not None, "can't parse __version__ from __init__.py"
    return version.group(1)


# -- Project information -----------------------------------------------------

project = 'coax'
copyright = '2020, Microsoft Corporation'
author = 'Kristian Holsheimer'
release = get_release()


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]


# autodoc settings
autodoc_default_options = {
    'members': True,
    'inherited-members': True,
    'special-members': '__call__',
}
autodoc_member_order = 'groupwise'  # by member type, falling back to bysource

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'examples/sandbox.ipynb', '**.ipynb_checkpoints', '_notebooks',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
# html_theme_path = ['_themes']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/img/coax_logo.png'
html_favicon = '_static/img/coax_favicon.png'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# options for
html_theme_options = {
    'canonical_url': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# get google analytics tracking id from: https://analytics.google.com
# add GA_TRACKING_ID env var to: https://readthedocs.org/dashboard/coax/environmentvariables/
# format: GA_TRACKING_ID=UA-XXXXXXX-1
if os.environ.get('GA_TRACKING_ID', '').startswith('UA-'):
    html_theme_options['analytics_id'] = os.environ['GA_TRACKING_ID']
    logger.info("added Google Analytics tracking ID to html_theme_options")

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]
html_js_files = [
    # 'js/custom.js',
]

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'coaxdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'coax.tex', 'coax Documentation',
     'Kristian Holsheimer', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'coax', 'coax Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'coax', 'coax Documentation',
     author, 'coax', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Options for nbsphinx extension ------------------------------------------

# don't evaluate any cells in ipython notebooks
nbsphinx_execute = 'never'


# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', ('_intersphinx/python3.inv',)),
    'numpy': ('https://docs.scipy.org/doc/numpy/', ('_intersphinx/numpy.inv',)),  # noqa: E501
    'sklearn': ('https://scikit-learn.org/stable/', ('_intersphinx/sklearn.inv',)),  # noqa: E501
    'jax': ('https://jax.readthedocs.io/en/latest/', ('_intersphinx/jax.inv',)),  # noqa: E501
    'haiku': ('https://dm-haiku.readthedocs.io/en/latest/', ('_intersphinx/haiku.inv',)),  # noqa: E501
    'rllib': ('https://rllib.readthedocs.io/en/latest/', ('_intersphinx/rllib.inv',)),  # noqa: E501
    'spinup': ('https://spinningup.openai.com/en/latest/', ('_intersphinx/spinup.inv',)),  # noqa: E501
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for napolean extension ------------------------------------------

# Defaults:
# napoleon_google_docstring = True
# napoleon_numpy_docstring = True
# napoleon_include_init_with_doc = False
# napoleon_include_private_with_doc = False
# napoleon_include_special_with_doc = True
# napoleon_use_admonition_for_examples = False
# napoleon_use_admonition_for_notes = False
# napoleon_use_admonition_for_references = False
# napoleon_use_ivar = False
# napoleon_use_param = True
# napoleon_use_rtype = True

# Overrides:
napoleon_use_rtype = False
napoleon_use_ivar = True
