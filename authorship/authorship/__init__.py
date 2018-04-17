import itertools

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from docutils.parsers.rst import directives


def generate_author_list(authors):
    return [
        nodes.Text(a, a)
        for a in authors
    ]


class Author(SphinxDirective):
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        env = self.state.document.settings.env

        env.authors.setdefault(env.docname, [])
        env.authors[env.docname].append(self.arguments[0])

        return []


class Authors(SphinxDirective):
    def run(self):
        env = self.state.document.settings.env
        return generate_author_list(env.authors.get(env.docname, []))


# maker node later to be replaced by list of all authors
class allauthors(nodes.General, nodes.Element):
    pass


class AllAuthors(SphinxDirective):
    def run(self):
        return [allauthors('')]


def builder_inited(app):
    app.builder.env.authors = {}


def purge_authors(app, env, docname):
    if not hasattr(env, 'authors'):
        return

    env.authors.pop(docname, None)


def process_authorlists(app, doctree, fromdocname):
    env = app.builder.env
    authors = set(itertools.chain(*[authors for authors in env.authors.values()]))

    for node in doctree.traverse(allauthors):
        node.replace_self(generate_author_list(authors))


def setup(app):
    app.add_node(allauthors)

    directives.register_directive('author', Author)
    directives.register_directive('authors', Authors)
    directives.register_directive('allauthors', AllAuthors)

    app.connect('builder-inited', builder_inited)
    app.connect('env-purge-doc', purge_authors)
    app.connect('doctree-resolved', process_authorlists)

    return {
        'version': '1.0.0',
    }
