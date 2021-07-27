# Authorship

Stores a list of authors and tags for each document.

The data is stored in the environment under the key ``authors`` and ``tags``.
It's a dictionary, where the keys are the names of the documents and the values
a list of author / tags.

## Authors

Use the ``.. author:: Author Name <email or url>`` directive to add an author to
a document. With ``.. author_list::`` you can add a paragraph, that list all
authors that are set for a document, like this::

    Written by: author1 <mail@some.org>, author2 <site.org>

### All Authors

The ``.. allauthors::`` directive generates an ordered list of all authors,
sorted by the number of contributions in descending order.

## Tags

Use the ``.. tag:: sometag`` directive to add a tag to a document. With ``..
tag_list::`` you can add a paragraph, that list all tags that are set for a
document, linking to the tag detail pages.
