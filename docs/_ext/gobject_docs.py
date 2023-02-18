# SPDX-FileCopyrightText: 2021 Fionn Kelleher
#
# SPDX-License-Identifier: CC0-1.0

"""
    developer_www.gidocgen
    ~~~~~~~~~~~~~~~~~~~~~~

    Allows referencing of GObject documentation via roles.

    This extension exists to standardise referencing external GObject docs
    within developer-www; in an event where the format of external GObject
    doc URLs changes, one can update this extension without needing to
    touch/replace anything in the reStructuredText markup.

    This particular implemention is programmed to generate references to
    documentation for websites generated with gi-docgen. As of writing, this
    includes docs.gtk.org.

    For more information about gi-docgen, please see:
    https://gitlab.gnome.org/GNOME/gi-docgen
"""

from urllib.parse import urljoin

from docutils.utils import unescape
from docutils import nodes
from sphinx.util.nodes import split_explicit_title


gidocgen_mappings = [
    "class",
    "iface",
    "struct",
    "alias",
    "enum",
    "flags",
    "error",
    "callback",
    "func",
    "const",
]

base_url_config_var = "gobject_docs_base_url"


def make_gobject_role(name, base_url):
    def role(type, rawtext, text, lineno, inliner, options={}, content={}):
        text = unescape(text)
        _, title, target = split_explicit_title(text)
        refuri = urljoin(base_url, "%s.%s.html" % (name, target))

        node = nodes.reference(title, title, internal=False, refuri=refuri)
        return [node], []

    return role


def setup_gobject_roles(app):
    for name, base_url in app.config[base_url_config_var].items():
        # allow referencing arbitrary docs (such as additional documentation)
        app.add_role("%s:doc" % name, make_gobject_role("", base_url))
        for mapping in gidocgen_mappings:
            role_name = "%s:%s" % (name, mapping)
            app.add_role(role_name, make_gobject_role(mapping, base_url))


def setup(app):
    app.add_config_value(base_url_config_var, {}, "env")
    app.connect("builder-inited", setup_gobject_roles)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parellel_write_safe": True
    }
