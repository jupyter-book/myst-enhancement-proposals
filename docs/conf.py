import json
import re

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.logging import getLogger

from pathlib import Path
from yaml import safe_load
import pandas as pd

LOGGER = getLogger(__name__)

project = "MyST Enhancement Proposals"
copyright = "2023, Executable Books Team"
author = "Executable Books Team"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
]
myst_enable_extensions = ["linkify"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


intersphinx_mapping = {
    "tc": ("https://compass.executablebooks.org/en/latest/", None),
}


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]

html_theme_options = {
    "logo": {
        "image_light": "_static/logo-wide.png",
        "image_dark": "_static/logo-wide-dark.png",
        "text": "Enhancement Proposals",
    },
    "icon_links": [
        {
            "url": "https://github.com/executablebooks/myst-enhancement-proposals",
            "icon": "fa-brands fa-github",
        },
        {
            "url": "https://executablebooks.org",
            "icon": "_static/eb-logo.png",
            "type": "local",
        },
        {
            "url": "https://compass.executablebooks.org",
            "icon": "fa-solid fa-compass",
        },
    ],
}

# -- Custom scripts -------------------------------------------------
# TODO: Could maybe re-use the metadata loading code we use in the transform?
root = Path(__file__).parent
meps = root / "meps"
table = []
for imep in meps.rglob("mep-*"):
    text = imep.read_text()
    yaml = text.split("---")[1].strip()
    yaml = safe_load(yaml)

    tablemd = {}
    tablemd["#"] = f"{yaml['mep']['id']}"
    tablemd["title"] = f"[{yaml['title']}]({imep.relative_to(root / 'meps')})"
    tablemd["created"] = yaml["mep"]["created"]
    tablemd["status"] = yaml["mep"]["status"]
    tablemd["discussion"] = f"[link]({yaml['mep']['discussion']})"
    table.append(tablemd)

# Write the table to a .txt file so that we can load it into the MEP index
path_md = root / "_build/dirhtml/meps.txt"
pd.DataFrame(table).to_markdown(path_md, index=None)
