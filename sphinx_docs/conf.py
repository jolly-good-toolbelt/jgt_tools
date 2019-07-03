"""Configure sphinx for package doc publication."""
import os
from pathlib import Path

import tomlkit

PYPROJECT_FILE = "pyproject.toml"
EXPLANATION = "- needed to extract version information."
file_path = Path(__file__).parents[1] / PYPROJECT_FILE

try:
    with open(file_path) as f:
        toml_data = tomlkit.parse(f.read())
except FileNotFoundError as e:
    print(f"Cannot find config file {file_path} {EXPLANATION}")
    print(e)
    exit(-1)

try:
    version = str(toml_data["tool"]["poetry"]["version"])
except KeyError as e:
    print(f"The [tool.poetry] 'version' key was not found {EXPLANATION}")
    print(e)
    exit(-1)

release = version

# PLEASE EDIT THE FOLLOWING CONFIGURATION INFORMATION:
######################################################

# General information about your project.
project = "JGT Tools - simple CLI package tools!"
copyright = "2018, Brad Brown"  # noqa
author = "Brad Brown"

######################################################
# BELOW HERE YOU SHOULD BE ABLE TO LEAVE AS-IS.


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.inheritance_diagram",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

html_theme_options = {
    "style_external_links": True,
    "titles_only": False,
    "collapse_navigation": False,
}


# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".tox",
    "*/.tox",
    ".eggs",
    "*/.eggs",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Include both class and init docstrings
autoclass_content = "both"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# If anyone wants to use another theme, they can change that here,
# but we consider that expert Sphinx user territory.
import sphinx_rtd_theme  # noqa

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]


def _owner_name_from(origin_url):
    """
    Extract the owner name from a git origin URL.

    The git origin URL might be in ``git+ssh`` form, or ``https`` form.

    Args:
        origin_url (str): Origin URL from `git`

    Returns:
        str: A slash-separated string containing the organization / owner and repository

    Examples:
        >>> owner_name_from("git@github.com:jolly-good-toolbelt/jgt_tools.git")
        "jolly-good-toolbelt/jgt_tools"
        >>> owner_name_from("https://github.com/jolly-good-toolbelt/jgt_tools.git")
        "jolly-good-toolbelt/jgt_tools"

    """
    if not origin_url:
        return ""
    owner_name = origin_url.split(":")[1]  # Remove method portion
    owner_name = owner_name.rsplit(".", 1)[0]  # Remove `.git`
    # Keep only the last two parts that remain, which are the org/owner and repo name
    return "/".join(owner_name.split("/")[-2:])


commit_id = os.environ.get("ghprbPullId") or os.environ.get("GIT_COMMIT_ID")
base_url = os.environ.get("ghprbPullLink") or ""
if not base_url:
    owner_name = _owner_name_from(os.environ.get("GIT_ORIGIN_URL", ""))
    if owner_name:
        base_url = f"https://github.com/{owner_name}/tree/{commit_id}"
html_context = {"build_id": commit_id, "build_url": base_url}
