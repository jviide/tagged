# tagged [![CircleCI](https://circleci.com/gh/jviide/tagged.svg?style=shield)](https://circleci.com/gh/jviide/tagged) [![PyPI](https://img.shields.io/pypi/v/tagged.svg?color=blue)](https://pypi.org/project/tagged/)

A Python version of JavaScript's [tagged templates](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#Tagged_templates), mixed with Python 3's [f-strings](https://docs.python.org/3/reference/lexical_analysis.html#f-strings).

## Installation

```sh
$ pip3 install tagged
```

## Usage

This package defines `tag`, that can be used as a decorator to create new tags. Let's define a boring one.

```py
from tagged import tag

@tag
def t(strings, values):
    return strings, values
```

Now `t` can be called with a template string that can contain any Python 3 expression between `{` and `}`. The "static" parts of the string are listed in `strings` and the evaluated expressions are listed in `values`.

```py
strings, values = t("1 + {2} equals {1 + 2}")
# strings == ('1 + ', ' equals ', '')
# values == (2, 3)
```

Because the expressions are evaluated in the current context they can refer to local variables:

```py
a = [1, 2, 3]
strings, values = t("the sum of {a} is {sum(a)}")
# strings == ('the sum of ', ' is ', '')
# values == ([1, 2, 3], 6)
```

Any Python 3 expression can be used

## rexample

Let's define a custom tag `rex` that allows composing regular expressions from strings and other regular expressions.

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
