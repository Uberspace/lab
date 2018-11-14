# Uberspace 7 Lab

Welcome to our laboratory! :tada:

This is where we host the source code of the official version over at https://lab.uberspace.de. The lab contains a collection of guides and tips on how to run specific software on Uberspace 7. Most of the guides are contributed by users like you! So, if you'd like to change or add something here, you're more than welcome to do so. Have a look at our [contributing guidelines](CONTRIBUTING.md) to learn how.

## Development

Pushing for each and every change is fun, but can take some
time. To speed up your development process, the lab can
be built locally.

### Initial Setup

```shell
$ virtualenv venv --python=python3.6
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Building

```shell
$ source venv/bin/activate
$ make html
```

The HTML views are now present in `build/html`.

## License

All text and code in this repository is licensed under [CC-BY-NC-SA 4.0][].
All project logos are property of the respective project.

[CC-BY-NC-SA 4.0]: https://creativecommons.org/licenses/by-nc-sa/4.0/
