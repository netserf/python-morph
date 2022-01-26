# python_sarlac v.0.2.2

[![Actions Status](https://github.com/netserf/python-sarlac/workflows/Test/badge.svg)](https://github.com/netserf/python-sarlac/actions)
[![Actions Status](https://github.com/netserf/python-sarlac/workflows/Markdown%20Lint/badge.svg)](https://github.com/netserf/python-sarlac/actions)
[![Actions Status](https://github.com/netserf/python-sarlac/workflows/Markdown%20Links/badge.svg)](https://github.com/netserf/python-sarlac/actions)

## What?

For those that don't like the one-liner awk or perl options, this is a command
line tool to help manage your string transformations through a yaml config file
and some understanding of regular expressions.

There are 2 ways the string transformations will be handled:

1. YAML configuration with an order of precedence:

    1. environment variable (SARLAC_CONFIG) set to configuration file location
    1. home directory with a .sarlac.yaml file
    1. /usr/local/etc/sarlac.yaml

1. CLI args for single ad-hoc transformations

Argument lists and stdin are both acceptable ways to input the string(s) to be
transformed.

## Why?

A number of my ops team members do not have a software development background,
but they are proficient on the command line. In their daily operations tasks
they often have to correct data issues that required simple stringo
transformations. Also, they may be called on to perform a set of batch string
transformations in their daily tasks. This tool is intended to help them
simplify these tasks and hopefully increase their productivity.

### Usage

```bash
$ sarlac --help
Usage: sarlac.py [OPTIONS] [CLI_ARGS]...

  A tool to help manage string transformations through a yaml config file
  and some understanding of regular expressions.

Options:
  -m, --match TEXT
  -r, --replace TEXT
  --help              Show this message and exit.
  ```

### Examples

```bash
$ echo "test123test" | sarlac --from "123" --to "456"
test456test

$ sarlac --from "123" --to "456" "test123test"
test456test

$ echo "test123test" | sarlac --from "\d+" --to "789"
test789test

$ echo "test123regex" | sarlac -f "(.*)\d+(.*)" -t "\1789\2"
test789regex
```

### Configuration

YAML config with order of precedence:

1. environment variable (SARLAC_CONFIG) set to configuration file location
1. home directory with a .sarlac.yaml file
1. /usr/local/etc/sarlac.yaml

Configuration file example - `sarlac.yaml`:

```yaml
---
substitutions:

    - name: Rule 0
      help: A simple match / replace rule
      match: match me
      replace: test 0

    - name: Rule 1
      help: A match/replace rule with a group match
      match: match me (.*) done
      replace: \1
```

### Installation

To build the wheel file:

```bash
pip install --upgrade setuptools wheel
pip install -r requirements-dev.txt
python setup.py bdist_wheel
```

To install the package:

```bash
pip install -r requirements.txt
pip install dist/[whl file] [--force-reinstall]
```

### Testing

```python
python setup.py test
```

## Requirements

- list package dependencies

## Future Improvements

TODO

## Authors

`python_sarlac` was written by `Greg Horie <networkserf@gmail.com>`
