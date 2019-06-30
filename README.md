# python_morph v.0.1.0

## What?
For those that don't like the one-liner awk or perl options, this is a command line tool to help manage your string transformations through a yaml config file and some understanding of regular expressions.

There are 2 ways the string transformations will be handled:
1) CLI args for one ad-hoc transformations
2) YAML configs with order of precedence
... 1 - local directory
... 2 - ~/.morph.conf
... 3 - /usr/local/etc

Argument lists and stdin are both acceptable ways to input the string(s) to be transformed.

## Why?
A number of my team members do not have software development skills, but they are proficient on the command line. In their daily operations tasks they often have to correct data issues that required simple string transformations. Also, they may be called on to perform a set of batch string transformations. This tool is intended to help them simplify these tasks and hopefully increase their productivity.

### Usage

TODO

### Examples
```
$ echo "test123test" | morph --from "123" --to "456"
test456test

$ morph --from "123" --to "456" "test123test" 
test456test

$ echo "test123test" | morph --from "\d+" --to "789"
test789test

$ echo "test123regex" | morph -f "(.*)\d+(.*)" -t "\1789\2"
test789regex
```

### Configuration
3) YAML config with order of precedence
... 1 - local directory
... 2 - ~/.morph.conf
... 3 - /usr/local/etc

### Installation

TODO

### Testing
```
$ python setup.py test
```

## Requirements

- list package dependencies

## Future Improvements

TODO

## Licence

## Authors
`python_morph` was written by `Greg Horie <networkserf@gmail.com>`_.

