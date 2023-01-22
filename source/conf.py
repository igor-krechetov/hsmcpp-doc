# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import re

project = 'HSMCPP'
copyright = '2021, Igor Krechetov'
author = 'Igor Krechetov'
# release = '0.26.0'
release = None
version = 'latest'

# -- Read version from hsmcpp sources ---------------------------------------
with open("./hsmcpp/CHANGELOG.md", "r") as f:
    lineNumber = 0
    for line in f:
        # NOTE: fix line number if changelog format will ever change
        if 3 == lineNumber:
            # format: ## [0.27.0] - 2023-01-20
            pattern = r"\[(\d+\.\d+\.\d+)\]"
            match = re.search(pattern, line)
            if match:
                release = match.group(1)
                print(f"{release=:}")
            break
        lineNumber += 1

if release is None:
    print(f"ERROR: hsmcpp version not found or it has incorrect format: '{line}'")
    exit(1)


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

# https://stackoverflow.com/questions/56336234/build-fail-sphinx-error-contents-rst-not-found
master_doc = 'index'

html_css_files = [
    'css/custom.css',
]

html_theme_options = {
    'navigation_depth': 4,
    'titles_only': True
}

# -- extlinks -------------------------------------------------
extlinks = {'repo-link': ('https://github.com/igor-krechetov/hsmcpp/blob/main%s', '%s')}

# -- sphinx_sitemap -------------------------------------------------
html_baseurl = 'https://hsmcpp.readthedocs.io/'
sitemap_url_scheme = "{lang}{version}{link}"
