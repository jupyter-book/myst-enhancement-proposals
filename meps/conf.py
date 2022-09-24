"""Configuration for building MEPs using Sphinx."""

project = "MEPs"
master_doc = "index"

extensions = [
    "myst_parser",
]

html_theme = "furo"
html_title = "MyST Enhancements Proposals"


# add a transform to check+use the front matter 'mep' data
import json

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.logging import getLogger

LOGGER = getLogger(__name__)


class FrontMatterTransform(SphinxTransform):
    """Use the front matter 'mep' data."""

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
        if not self.env.docname.startswith("mep-"):
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
        required_keys = ["id", "created", "author", "type", "status", "discussions-to"]
        optional_keys = [
            "sponsor",
            "mep-delegate",
            "requires",
            "replaces",
            "superseded-by",
        ]
        missing = set(required_keys).difference(data)
        if missing:
            raise ValueError(
                f"'mep' front-matter does not contain all required keys: {missing}"
            )
        # split authors
        if isinstance(data["author"], str):
            data["author"] = [data["author"]]
        data["author"] = ", ".join(data["author"])
        # find first title
        for title_node in self.document.findall(nodes.title):
            break
        else:
            raise ValueError("no title found")
        title_node.insert(0, nodes.Text(f"MEP {data['id']} - "))

        # create a docutils table of the metadata, just under the heading
        table = nodes.table(classes=["align-left"])
        tgroup = nodes.tgroup(cols=2)
        table += tgroup
        tgroup += nodes.colspec(colwidth=50)
        tgroup += nodes.colspec(colwidth=50)
        thead = nodes.thead()
        tgroup += thead
        tbody = nodes.tbody()
        tgroup += tbody
        for key in required_keys + optional_keys:
            if key == "id" or key not in data:
                continue
            value = data[key]
            tbody += nodes.row(
                "",
                nodes.entry("", nodes.Text(key.capitalize()), classes=["text-left"]),
                nodes.entry("", nodes.Text(str(value)), classes=["text-left"]),
            )
        title_node.parent.insert(title_node.parent.index(title_node) + 1, table)


def setup(app):
    app.add_transform(FrontMatterTransform)
