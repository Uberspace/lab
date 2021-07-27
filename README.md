# Uberspace 7 Lab

Welcome to our laboratory! :tada:

This is where we host the source code of the official version over at
https://lab.uberspace.de. The lab contains a collection of guides and tips on
how to run specific software on Uberspace 7. Most of the guides are contributed
by users like you! So, if you'd like to change or add something here, you're
more than welcome to do so. Have a look at our [contributing guidelines][] to
learn how. Also, have a look at the [list of guides][] people are looking for!

## Development

Pushing for each and every change is fun, but can take some time. To speed up
your development process, the lab can be built locally.

### Initial Setup

```shell
make setup
```

### Building

```shell
$ source .venv/bin/activate
$ make clean html
```

The HTML views are now present in `build/html`.

### Development Server

To build automatically on each change use `sphinx-autobuild`:

```
$ make clean serve
```

This will start a local webserver on http://127.0.0.1:8000, which always serves
the most recent version.

### Spellcheck

To check the spelling you can use the spell check function of sphinx.

```
$ make spelling
```

## License

All text and code in this repository is licensed under [CC-BY-NC-SA 4.0][].
All project logos are property of the respective project.

[CC-BY-NC-SA 4.0]: https://creativecommons.org/licenses/by-nc-sa/4.0/
[contributing guidelines]: CONTRIBUTING.md
[list of guides]: https://github.com/Uberspace/lab/issues?q=is%3Aopen+is%3Aissue+label%3Aguide
