import itertools

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
import sphinx.addnodes as addnodes
from docutils.parsers.rst import directives


def comma_list(nodes_):
    elements = []

    if not nodes_:
        return []

    for node in nodes_:
        elements.append(node)
        elements.append(nodes.Text(', '))

    return elements[:-1]

class Tag(SphinxDirective):
    required_arguments = 1
    final_argument_whitespace = True

    def run(self):
        env = self.state.document.settings.env

        env.tags.setdefault(env.docname, [])
        env.tags[env.docname].append(self.arguments[0])

        return []


class Tags(SphinxDirective):
    def run(self):
        env = self.state.document.settings.env
        tags = env.tags.get(env.docname, [])

        if not tags:
            return []

        return [nodes.Text('Tags: ')] + comma_list(nodes.Text(t) for t in tags)

# maker node later to be replaced by list of all tags
class alltags(nodes.General, nodes.Element):
    pass


class AllTags(SphinxDirective):
    def run(self):
        return [alltags('')]


def builder_inited(app):
    app.builder.env.tags = {}


def purge_tags(app, env, docname):
    if not hasattr(env, 'tags'):
        return

    env.tags.pop(docname, None)


def process_taglists(app, doctree, fromdocname):
    env = app.builder.env
    tags = set(itertools.chain(*[tags for tags in env.tags.values()]))
    guides_by_tag = {
        t: set(g for g, guide_tags in env.tags.items() if t in guide_tags)
        for t in tags
    }

    for node in doctree.traverse(alltags):
        lst = nodes.bullet_list()

        for tag in tags:
            lst_item = nodes.list_item()
            lst += lst_item
            lst_item += addnodes.compact_paragraph(text=tag)

            lst_item += nodes.raw('', '<br>', format='html')

            links = []

            for guide in guides_by_tag[tag]:
                # I can't figure out a way to get the link and title from a page name..
                link = guide + '.html'
                title = guide.partition('_')[2].title()

                link_wrapper = addnodes.compact_paragraph()
                link_wrapper += nodes.reference('', '', nodes.Text(title), internal=True, refuri=link, anchorname='')

                links.append(link_wrapper)

            for n in comma_list(links):
                lst_item += n

        node.replace_self([lst])


def setup(app):
    app.add_node(alltags)

    directives.register_directive('tag', Tag)
    directives.register_directive('tags', Tags)
    directives.register_directive('alltags', AllTags)

    app.connect('builder-inited', builder_inited)
    app.connect('env-purge-doc', purge_tags)
    app.connect('doctree-resolved', process_taglists)

    return {
        'version': '1.0.0',
    }
