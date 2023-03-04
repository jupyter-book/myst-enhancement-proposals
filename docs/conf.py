import json
import re

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.logging import getLogger

from pathlib import Path
from yaml import safe_load
import pandas as pd

project = "MyST Enhancement Proposals"
copyright = "2023, Executable Books Team"
author = "Executable Books Team"

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
]
myst_enable_extensions = ["colon_fence", "deflist", "linkify"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


intersphinx_mapping = {
    "tc": ("https://compass.executablebooks.org/en/latest/", None),
}


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_favicon = "_static/eb-logo.png"

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

LOGGER = getLogger(__name__)

##
# Add a table index of all of our MEPs we insert into a few places.
##

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
    tablemd["title"] = f"[{yaml['title']}](/{imep.relative_to(root)})"
    tablemd["created"] = yaml["mep"]["created"]
    tablemd["status"] = yaml["mep"]["status"]
    tablemd["discussion"] = f"[link]({yaml['mep']['discussion']})"
    table.append(tablemd)

# Write the table to a .txt file so that we can load it into the MEP index
path_md = root / "_build/dirhtml/meps.txt"
path_md.parent.mkdir(exist_ok=True, parents=True)
pd.DataFrame(table).to_markdown(path_md, index=None)


##
# Add a frontmatter table to the top of each MEP.
##
class FrontMatterTransform(SphinxTransform):
    default_priority = 1000

    def apply(self):
        try:
            self.use_frontmatter()
        except Exception as exc:
            LOGGER.warning(
                str(exc),
                location=(self.env.docname, 0),
                type="mep",
                subtype="frontmatter",
            )

    def use_frontmatter(self):
        if not self.env.docname.startswith("meps/mep-"):
            return
        node = self.document[0]
        if not isinstance(node, nodes.field_list):
            raise ValueError("no metadata found")
        meta = None
        for field in node:
            if field[0].astext() == "mep":
                meta = field[1].astext()
                break
        if meta is None:
            raise ValueError("no 'mep' front-matter key found")
        try:
            data = json.loads(meta)
        except Exception as exc:
            raise ValueError(f"could not read front matter: {exc}")

        # Some basic validation to make sure the required fields are there
        required_keys = ["id", "created", "authors", "status", "discussion"]
        missing = set(required_keys).difference(data)
        if missing:
            raise ValueError(
                f"'mep' front-matter does not contain all required keys: {missing}"
            )
        # check type/status enums
        if data["status"] not in (
            "Draft",
            "Active",
            "Accepted",
            "Not Accepted",
        ):
            raise ValueError(f"invalid 'status' value: {data['status']}")
        # ensure date is a string
        data['created'] = str(data['created'])
        # check 'created' value in right format (YYYY-MM-DD)
        if not re.fullmatch(r"\d\d\d\d-\d\d-\d\d", data["created"]):
            raise ValueError(
                f"invalid 'created' value (not YYYY-MM-DD): {data['created']}"
            )

        # split authors
        if isinstance(data["authors"], str):
            data["authors"] = [data["authors"]]
        data["authors"] = ", ".join(data["authors"])

        # Find the first title in the page so we'll put the table underneath
        for title_node in self.document.findall(nodes.title):
            break
        else:
            raise ValueError("no title found")
        title_node.insert(0, nodes.Text(f"MEP {data['id']} - "))

        # create a docutils table of the metadata, just under the heading
        table = nodes.table(classes=["mep-metadata align-left"])
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=50)
        tgroup += nodes.colspec(colwidth=50)
        thead = nodes.thead()
        tgroup += thead
        tbody = nodes.tbody()
        tgroup += tbody
        for key in required_keys:
            if key == "id" or key not in data:
                continue
            value = data[key]
            if key == "discussion":
                value_node = nodes.inline()
                value_node += nodes.reference("", nodes.Text(str(value)), refuri=value)
            else:
                value_node = nodes.Text(str(value))
            tbody += nodes.row(
                "",
                nodes.entry("", nodes.Text(key.capitalize()), classes=["text-left"]),
                nodes.entry("", value_node, classes=["text-left"]),
            )
        title_node.parent.insert(title_node.parent.index(title_node) + 1, table)


def setup(app):
    app.add_transform(FrontMatterTransform)
