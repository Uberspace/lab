# Lab

The UberLab aims to provide various tutorials on how to
setup tools and software inside an uberspace on U7.

## Development

Pushing for each and every change is fun, but can take some
time. To speed up your development process, the lab can
be built locally.

### Initial Setup

```
$ virtualenv venv --python=python2.7
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Building

```
$ source venv/bin/activate
$ make html
```

The HTML views are now present in `build/html`. 

## License

All text and code in this repository is licensed under [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
All project logos are property of the respective project.
