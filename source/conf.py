# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import re
import subprocess
from subprocess import call
import shutil
import sys
from textwrap import dedent
from exhale import utils
from bs4 import BeautifulSoup

project = 'HSMCPP'
copyright = '2021, Igor Krechetov'
author = 'Igor Krechetov'
release = None
version = 'latest'
on_rtd = os.environ.get('READTHEDOCS') == 'True'

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

# -- Environment ------------------------------------------------------------
sourcePath = os.path.dirname(os.path.realpath(__file__))
buildDir = f"{sourcePath}/_build"
apiDir = f"{sourcePath}/api"

# -- Doxygen ----------------------------------------------------------------
shutil.copy("./Doxyfile.in", "./Doxyfile")
try:
    os.mkdir(buildDir)
except:
    print(f"{buildDir} already exists")

try:
    os.mkdir(apiDir)
except:
    print(f"{apiDir} already exists")

with open("./Doxyfile", "a") as fDoxygenConfig:
    # Tell doxygen to output wherever breathe is expecting things
    extraConfig = [f"OUTPUT_DIRECTORY = \"{buildDir}/doxygen\"\n",
                   # Tell doxygen to strip the path names (RTD builds produce long abs paths...)
                   f"STRIP_FROM_PATH  = \"{sourcePath}/hsmcpp\"\n"]
    fDoxygenConfig.writelines(extraConfig)

subprocess.call('doxygen ./Doxyfile', cwd=f"{sourcePath}", shell=True)
# shutil.rmtree(f"{sourcePath}/../build/doxygen", ignore_errors=True)
# shutil.move(f"{sourcePath}/hsmcpp/doxygen", f"{sourcePath}/../build")

# Due to a bug in sphinxcontrib.doxylink we need to fix generated TAG file
# plugin doesn't understand template variadic arguments with "..."
hsmcppTagFile = f"{apiDir}/hsmcpp.tag"

with open(hsmcppTagFile, "r+") as file:
    text = file.read()
    text = text.replace("Args...", "Args")
    file.seek(0)
    file.write(text)
    file.truncate()


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = ['sphinx.ext.extlinks', 'sphinxemoji.sphinxemoji', 'm2r2',
              'sphinxcontrib.plantuml', 'sphinx_sitemap', 'breathe', 'exhale',
              'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinxcontrib.doxylink']

templates_path = ['_templates']
exclude_patterns = ['hsmcpp']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_extra_path = ["_seo"]

# https://stackoverflow.com/questions/56336234/build-fail-sphinx-error-contents-rst-not-found
master_doc = 'index'

html_css_files = ['css/custom.css']

# html_theme_options = {
#     'navigation_depth': 4,
#     'titles_only': True
# }

# Tell sphinx what the primary language being documented is.
primary_domain = 'cpp'

pygments_style = "sphinx"

html_show_sourcelink = False

# -- sphinxcontrib.plantuml ---------------------------------------------------
if on_rtd:
    # Version of PlantUML on ReadTheDocs is too old, so using our own
    plantumlBin = f"{sourcePath}/../tools/plantuml.jar"
    # plantUmlBin = "/usr/share/plantuml/plantuml.jar"
    plantuml = f"java -Djava.awt.headless=true -jar {plantumlBin}"
else:
    plantuml = '/usr/bin/plantuml'

plantuml_output_format = 'png'

# -- extlinks -------------------------------------------------
extlinks = {'repo-link': ('https://github.com/igor-krechetov/hsmcpp/blob/main%s', '%s')}

# -- sphinx_sitemap ------------------------------------------------
html_baseurl = 'https://hsmcpp.readthedocs.io/'
sitemap_url_scheme = "{lang}{version}{link}"

# -- breathe --------------------------------------------------------
breathe_default_project = "hsmcpp"
breathe_projects = {'hsmcpp': './_build/doxygen/xml'}
breathe_separate_member_pages = True

# -- doxylink ------------------------------------------------------
doxylink = {
    'hsmcpp' : (hsmcppTagFile, './api'),
}

def postprocessDoxylinks(app, pagename, templatename, context, doctree):
    if (pagename.startswith("api/class") == False) and ("body" in context):
        contentChanged = False
        soup = BeautifulSoup(context['body'], 'html.parser')
        patternUrl = r"/api/(class.*)\.html#(.*)"

        for el in soup.find_all("a", class_="reference external"):
            # example: ../.././api/classhsmcpp_1_1HierarchicalStateMachine.html#a5f006e704e2958793a03efc4eadcbb6f
            if ("href" in el.attrs) and ("/api/class" in el["href"]):
                match = re.search(patternUrl, el["href"])
                if match:
                    pageId = match.group(1)
                    itemId = match.group(2)
                    el["href"] = el["href"].replace(itemId, f"{pageId}_1{itemId}")
                    contentChanged = True
                    # exit(1)
        if True == contentChanged:
            context['body'] = str(soup)


# -- exhale ---------------------------------------------------------
def specificationsForKind(kind):
    '''
    For a given input ``kind``, return the list of reStructuredText specifications
    for the associated Breathe directive.
    '''
    # Change the defaults for .. doxygenclass:: and .. doxygenstruct::
    if kind == "class" or kind == "struct":
        return [
          ":members:",
          ":undoc-members:",
        ]
    # Change the defaults for .. doxygenenum::
    elif kind == "enum":
        return [":no-link:"]
    # An empty list signals to Exhale to use the defaults
    else:
        return []


def prepareHtmlString(value):
    return value.strip(", ").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# exhale and breathe does not seem to provide a way to generate TOC for a class in a similar way as Doxygen does it.
# so we'll parse generated page and inject TOC ourself.
# NOTE: probably will not work with anything except sphinx_rtd_theme, but can be easily adapted (if needed)
def postprocessClassFiles(app, pagename, templatename, context, doctree):
    if pagename.startswith("api/class"):
        soup = BeautifulSoup(context['body'], 'html.parser')
        # templates are generated as separate entities so we need to ignore them
        # ignoreItems = ["Args", "HsmHandlerClass"]
        ignoreItems = []
        # markers to parse different types
        sectionMarkers = [{"title": "Public Types", "type": "enum", "class": "cpp enum-class", "prefix": "enum "},
                          {"title": "Public Member Functions", "type": "function", "class": "cpp function", "prefix": ""}]
        newContent = ""
        separator = "<tr><td class=\"api-table-func-separator\" colspan=\"2\">&nbsp;</td></tr>"

        for section in sectionMarkers:
            currentSectionBody = ""
            # insert separators between functions
            marker = f"<dl class=\"{section['class']}\">"
            context['body'] = context['body'].replace(marker, "<hr />" + marker)

            for el in soup.find_all(class_=section["class"]):
                elName = el.find(class_="sig-name descname")
                if elName and elName.get_text() not in ignoreItems:
                    elObject = el.find("dt", class_="sig sig-object cpp")
                    elDescription = el.find("dd")
                    strDescription = ""
                    elLink = el.find("a", class_="headerlink")

                    if elDescription:
                        for par in elDescription.findChildren(recursive=False):
                            strDescription = par.get_text()
                            break

                    if elObject and elLink:
                        strReturn = ""
                        strName = ""
                        strArgs = ""
                        temp = ""
                        skipNode = True

                        if section["type"] == "function":
                            for elNamePart in elObject.contents:
                                if hasattr(elNamePart, 'attrs'):
                                    if "class" in elNamePart.attrs:
                                        if skipNode == False:
                                            if "sig-name" in elNamePart["class"]:
                                                strReturn = prepareHtmlString(temp)
                                                temp = ""
                                            elif "sig-paren" in elNamePart["class"]:
                                                if len(strName) == 0:
                                                    strName = prepareHtmlString(temp)
                                                    temp = ""
                                                else:
                                                    strArgs = f" {prepareHtmlString(temp)})"
                                                    break

                                            temp += elNamePart.get_text()
                                        elif "target" in elNamePart["class"]:
                                            skipNode = False
                                elif "," in elNamePart.get_text():
                                    temp += elNamePart.get_text()
                        elif section["type"] == "enum":
                            strName = elName.get_text()

                        if len(strName) > 0:
                            currentSectionBody += f"<tr><td class=\"api-table-func-return\">{section['prefix']}{strReturn}</td><td><a class=\"api-table-func-url\" href=\"{elLink['href']}\">{strName}</a>{strArgs}</td></tr>"
                            if len(strDescription) > 0:
                                currentSectionBody += f"<tr><td>&nbsp;</td><td class=\"api-table-func-brief\">{strDescription}</td></tr>"
                            currentSectionBody += separator

            if len(currentSectionBody) > 0:
                newContent += f"<div class=\"contents local topic\"><p class=\"topic-title\">{section['title']}</p>"
                newContent += "<table>"
                newContent += separator + currentSectionBody
                newContent += '</table></div><br />'

        # insert TOC before main body
        if soup.find(id="nested-relationships"):
            marker = '<section id="nested-relationships">'
        elif soup.find(id="inheritance-relationships"):
            marker = '<section id="inheritance-relationships">'
        else:
            marker = '<section id="class-documentation">'

        context['body'] = context['body'].replace(marker, newContent + "\n" + marker)


exhale_args = {
    # Mandatory arguments
    "containmentFolder":     "./api",
    "rootFileName":          "api.rst",
    "doxygenStripFromPath":  "./hsmcpp",
    # Optional arguments
    "rootFileTitle":         "API Reference",
    "createTreeView":        True,
    # Doxygen arguments
    "exhaleExecutesDoxygen": False,
    # "exhaleSilentDoxygen": False,
    # "exhaleDoxygenStdin": dedent('''
    #     INPUT   = ./hsmcpp/include
    #     EXCLUDE_PATTERNS = FreeRTOSConfig.h FreeRtosPort.hpp logging.hpp */os/*
    #     EXCLUDE_SYMBOLS = hsmcpp::HsmEventDispatcherBase::TimerInfo hsmcpp::HsmEventDispatcherBase::EnqueuedEventInfo HsmEventDispatcherArduino::RunningTimerInfo HsmEventDispatcherSTD::RunningTimerInfo
    #     EXTRACT_PRIVATE = NO
    #     HIDE_UNDOC_MEMBERS = NO
    #     HIDE_UNDOC_CLASSES = YES
    #     INTERNAL_DOCS = NO
    #     XML_PROGRAMLISTING = YES
    # '''),
    "customSpecificationsMapping": utils.makeCustomSpecificationsMapping(
        specificationsForKind
    ),
    ############################################################################
    # Main library page layout configuration.                                  #
    ############################################################################
    # "afterTitleDescription": dedent(u'''
    # '''),
    # "afterHierarchyDescription": dedent('''
    # '''),
    "fullApiSubSectionTitle": "API List",
    # "afterBodySummary": dedent('''
    # '''),
    ############################################################################
    # Individual page layout configuration.                                    #
    ############################################################################
    "contentsDirectives": True,
    "contentsTitle": "Content",
    "kindsWithContentsDirectives": ["class", "file", "namespace", "struct"],
    "includeTemplateParamOrderList": True,
    ############################################################################
    "verboseBuild": True
}


# -- post-processing ----------------------------------------------------
def onHtmlPageContext(app, pagename, templatename, context, doctree):
    postprocessClassFiles(app, pagename, templatename, context, doctree)
    postprocessDoxylinks(app, pagename, templatename, context, doctree)


def setup(app):
    # install context callback
    app.connect('html-page-context', onHtmlPageContext)