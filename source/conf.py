# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os

project = 'HSMCPP'
copyright = '2023, Igor Krechetov'
author = 'Igor Krechetov'
release = '0.26.0'
version = 'latest'


# -- PlantUML Integration ---------------------------------------------------
on_rtd = os.environ.get('READTHEDOCS') == 'True'

if on_rtd:
    plantuml = 'java -Djava.awt.headless=true -jar /usr/share/plantuml/plantuml.jar'
else:
    plantuml = '/usr/bin/plantuml'

plantuml_output_format = 'png'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.extlinks', 'sphinxemoji.sphinxemoji', 'm2r2', 'sphinxcontrib.plantuml', 'sphinx_sitemap']

templates_path = ['_templates']
exclude_patterns = ['hsmcpp']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
# html_theme = 'alabaster'
html_static_path = ['_static']
html_extra_path = ["_seo"]


html_css_files = [
    'css/custom.css',
]

html_theme_options = {
    'analytics_id': 'G-8948Z3LWSQ',
    'navigation_depth': 4,
    'titles_only': True
}

# -- extlinks -------------------------------------------------
extlinks = {'repo-link': ('https://github.com/igor-krechetov/hsmcpp/blob/main%s', '%s')}

# -- sphinx_sitemap -------------------------------------------------
html_baseurl = 'https://hsmcpp.readthedocs.io/'
sitemap_url_scheme = "{lang}{version}{link}"
