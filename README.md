# Uberspace 7 Lab

Welcome to our laboratory! :tada:

This is where we host the source code of the official version over at
<https://lab.uberspace.de>. The lab contains a collection of guides and tips on
how to run specific software on Uberspace 7. Most of the guides are contributed
by users like you! So, if you'd like to change or add something here, you're
more than welcome to do so. Have a look at our [contributing guidelines][] to
learn how. Also, have a look at the [list of guides][] people are looking for!

## Prerequisites

**Note:** When using VS Code with the [devcontainer](https://containers.dev/), you only need to have [Docker](https://docs.docker.com/desktop/) installed.

Simply open the repository in VS Code and press `F1` to open the command palette, then select `Remote-Containers: Reopen in Container` to open the repository in a container.

The devcontainer will have all the necessary dependencies installed, and will automatically run the initial setup.

Generally, you need to have installed:

-   Python (<= 3.11)
-   [Enchant library](https://rrthomas.github.io/enchant/)

## Development

Pushing for each and every change is fun, but can take some time. To speed up
your development process, the lab can be built locally.

### Initial Setup

```shell
make setup
```

### Building

```shell
source .venv/bin/activate
make clean html
```

The HTML views are now present in `build/html`.

### Development Server

To build automatically on each change use `sphinx-autobuild`:

```shell
make clean serve
```

This will start a local webserver on http://127.0.0.1:8000, which always serves
the most recent version.

## Linting

To lint all files, you can use `pre-commit`:

```shell
make lint
```

Or just to check the guides for consistency:

```shell
make check-guides
```

## Spellcheck

To check the spelling you can use the spell check function of Sphinx:

```shell
make spelling
```

### Add Words to Guide

If your guide needs to use words, that should not go into the _global
dictionary_ (see below), you can flag them with the `spelling` directive like
this (usually near the top of your guide):

```rst
.. spelling::
    passwörd
    anotherword
```

### Add Words to Global Dictionary

1. run `make get-new-words` to write a list of all spelling errors found
   to `new_words.txt`
1. edit the resulting `new_words.txt`
    1. decide wich words to keep for the global dict,
    1. and wich might be better put into a guide local list (see the `spelling`
       directive above for that)
1. if satisfied, run `make add-new-words` to merge them to the global dictionary
1. commit your changes :pencil2:

## License

All text and code in this repository is licensed under [CC-BY-NC-SA 4.0][].
All project logos are property of the respective project.

[cc-by-nc-sa 4.0]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[contributing guidelines]: CONTRIBUTING.md
[list of guides]: https://github.com/Uberspace/lab/issues?q=is%3Aopen+is%3Aissue+label%3Anew-guide
