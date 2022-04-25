"""
Authorship — Stores a list of authors for each document.

The data is stored in the environment under the key ``authors``. It's a
dictionary, where the keys are the names of the documents and the values a list
of author names.

"""
import itertools
import os.path
import re

import sphinx.addnodes as addnodes
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective


def comma_list(nodes_, separator):
    """Return list of nodes seperated by `, ` text nodes."""
    elements = []

    if not nodes_:
        return []

    for node in nodes_:
        elements.append(node)
        elements.append(nodes.Text(separator))

    return elements[:-1]


class ListItem(SphinxDirective):
    """
    Store a list of things (e.g. authors, tags) in the environment of each
    document.

    """

    required_arguments = 1
    final_argument_whitespace = True

    marker_list_name = None

    def run(self):
        assert self.marker_list_name

        env = self.state.document.settings.env
        l = getattr(env, self.marker_list_name)

        l.setdefault(env.docname, [])
        l[env.docname].append(self.arguments[0])

        return []


class AuthorListDisplay(SphinxDirective):
    """
    Output the list of authors for the document.

    Like: `Written by: author1 <mail@some.org>, author2 <site.org>`

    From rst markup like::

        .. author_list::

    """

    def run(self):
        env = self.state.document.settings.env
        items = env.author_list.get(env.docname, [])
        item_nodes = (nodes.Text(a) for a in items)

        if items:
            return (
                [nodes.Text("Written by: ")]
                + comma_list(item_nodes, ", ")
                + [nodes.raw("", "<br>", format="html")]
            )
        else:
            return []


class TagListDisplay(SphinxDirective):
    """
    Output the list of tags for the document.

    Like: `#lang-nodejs #web`

    From rst markup like::

        .. tag_list::

    """

    def run(self):
        env = self.state.document.settings.env

        container = nodes.container()
        container.set_class("taglist")

        for item in sorted(env.tag_list.get(env.docname, []), key=str.lower):
            elem = nodes.inline()
            elem += nodes.reference("", "#" + item, refuri="/tags/" + item)
            elem.set_class("tag")
            container += elem
            container += nodes.raw("", "&nbsp;", format="html")

        return [container]


def add_list_type(app, name, list_cls):
    """
    Register directives for *name* with *list_cls* and connect them with *app*.

    1. Register directive `<name>`: it stores entries in the environemnt under
       the key `<name>_list` (by subclassing :cls:`ListItem`).

    1. Register directive `<name>_list`: it outputs the stored elements as
       goverend by *list_class*.

    1. Connect handlers for the directives.

    """
    list_name = name + "_list"

    class ListItemImpl(ListItem):
        marker_list_name = list_name

    def init_list(app):
        """Initialize environment."""
        setattr(app.builder.env, list_name, {})

    def purge(app, env, docname):
        """Remove possible stale info for updated documents."""
        if hasattr(env, list_name):
            getattr(env, list_name).pop(docname, None)

    directives.register_directive(name, ListItemImpl)
    directives.register_directive(list_name, list_cls)

    app.connect("builder-inited", init_list)
    app.connect("env-purge-doc", purge)


class allauthors(nodes.General, nodes.Element):
    """Maker node later to be replaced by list of all authors."""

    pass


class AllAuthors(SphinxDirective):
    """
    Outputs an ordered list of all authors, sorted by contribution count.

    From rst markup like::

        .. allauthors::

    """

    def run(self):
        return [allauthors("")]


def process_authorlists(app, doctree, fromdocname):
    """Build list of authors sorted by contribution count."""
    env = app.builder.env
    authors = set(itertools.chain(*[authors for authors in env.author_list.values()]))
    guides_by_author = {
        a: set(g for g, guide_authors in env.author_list.items() if a in guide_authors)
        for a in authors
    }
    count_by_author = {a: len(guides_by_author[a]) for a in authors}

    for node in doctree.traverse(allauthors):
        author_list = nodes.enumerated_list(classes=["hof__list"])

        for author, count in sorted(
            count_by_author.items(), key=lambda x: (-x[1], x[0].lower())
        ):
            # list entry
            author_entry = nodes.list_item(classes=["hof__entry"])
            author_list += author_entry

            # counter
            counter_div = nodes.container(classes=["hof__counter"])
            counter_div += addnodes.compact_paragraph(text=count)
            author_entry += counter_div

            # author
            author_div = nodes.container(classes=["hof__author"])
            author_div += addnodes.compact_paragraph(text=author)
            author_entry += author_div

            # guide list
            guides_div = nodes.container(classes=["hof__guides"])
            author_entry += guides_div

            # linklist
            guides_list = nodes.bullet_list(classes=["hof__guide_list"])
            guides_div += guides_list

            for guide in sorted(guides_by_author[author]):
                # guide
                link_entry = nodes.list_item(classes=["hof__guide"])
                guides_list += link_entry

                # I can't figure out a way to get the link and title from a page name..
                link = '/' + guide + '.html'
                title = guide.partition("_")[2].title()

                link_wrapper = addnodes.compact_paragraph()
                link_wrapper += nodes.reference(
                    "", "", nodes.Text(title), internal=True, refuri=link, anchorname=""
                )
                link_entry += link_wrapper

        node.replace_self([author_list])


def tag_list(app):
    env = app.builder.env
    tags = sorted(
        set(itertools.chain(*[tags for tags in env.tag_list.values()])), key=str.lower
    )

    return [
        (
            "tags/index",
            {
                "tags": tags,
                "title": "Tags",
            },
            "tags.html",
        )
    ]


def tag_intro(tag):
    intro_file = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "../../source/tags", tag + ".txt")
    )

    try:
        with open(intro_file) as f:
            intro = f.read()

        # replace #tags with links to their tag pages
        intro = re.sub(r"#([a-z0-9]+)", r'<a href="/tags/\1">#\1</a>', intro)

        return intro
    except OSError:
        return ""


def tag_pages(app):
    env = app.builder.env
    tags = set(itertools.chain(*[tags for tags in env.tag_list.values()]))
    guides_by_tag = {
        t: set(g for g, guide_tags in env.tag_list.items() if t in guide_tags)
        for t in tags
    }

    return [
        (
            "tags/" + t,
            {
                "tag": t,
                "parents": [{"title": "Tags", "link": "/tags"}],
                "title": "#" + t,
                "guides": guides_by_tag[t],
                "titles": env.titles,
                "intro": tag_intro(t),
            },
            "tag.html",
        )
        for t in guides_by_tag
    ]


def setup(app):
    add_list_type(app, "author", AuthorListDisplay)
    app.add_node(allauthors)
    directives.register_directive("allauthors", AllAuthors)
    app.connect("doctree-resolved", process_authorlists)

    add_list_type(app, "tag", TagListDisplay)
    app.connect("html-collect-pages", tag_pages)
    app.connect("html-collect-pages", tag_list)

    return {
        "version": "1.0.0",
    }
