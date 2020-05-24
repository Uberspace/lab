# Authorship

Stores a list of authors for each document.

The data is stored in the environment under the key ``authors``. It's a
dictionary, where the keys are the names of the documents and the values a list
of author names.

## Usage

Use the ``.. author:: Author Name <email or url>`` directive to add information
to a document. With ``.. author_list::`` you can add a paragraph, that list all
authors that are set for a document, like this::

    Written by: author1 <mail@some.org>, author2 <site.org>

The ``.. allauthors::`` directive generates an ordered list of all authors,
sorted by the number of contributions in descending order.
