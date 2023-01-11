# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'hsmcpp'
copyright = '2023, Igor Krechetov'
author = 'Igor Krechetov'
release = '0.26.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.extlinks', 'sphinxemoji.sphinxemoji', 'm2r2']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_theme = 'alabaster'
html_static_path = ['_static']

html_css_files = [
    'css/custom.css',
]


# -- extlinks -------------------------------------------------
extlinks = {'repo-link': ('https://github.com/igor-krechetov/hsmcpp/blob/main%s', '%s')}
