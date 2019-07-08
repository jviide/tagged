# tagged [![CircleCI](https://circleci.com/gh/jviide/tagged.svg?style=shield)](https://circleci.com/gh/jviide/tagged)

A Python version of JavaScript's tagged templates.

## Installation

```sh
$ pip3 install tagged
```

## Usage

```py
import re
from tagged import tag


@tag
def rex(strings, values):
    pattern = strings[0]
    for value, string in zip(values, strings[1:]):
        if isinstance(value, re.Pattern):
            value = value.pattern
        elif isinstance(value, str):
            value = re.escape(value)
        else:
            raise TypeError("expected re.Pattern or str")
        pattern += "(?:" + value + ")" + string
    return re.compile(pattern)


greeting = re.compile("Hello|Hi|Greetings")
name = "Python 3.7"
rex("{greeting}, {name}!")
# re.compile('(?:Hello|Hi|Greetings), (?:Python\\ 3\\.7)!')
```

## Development

### Running Tests

```sh
$ python3 -m unittest discover -s tests
```

## License

This library is licensed under the MIT license. See [./LICENSE](./LICENSE).
