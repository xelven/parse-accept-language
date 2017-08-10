# parse-accept-language

[![PyPI version](https://badge.fury.io/py/parse-accept-language.svg)](https://badge.fury.io/py/parse-accept-language)


Parse Accept-Language HTTP header.

## Installation

```bash
pip install parse-accept-language
```

## How To Use

```python
from accept_language import parse_accept_language

>>> parse_accept_language('es-mx;q=0.8,es,en')
[
    Lang(locale=None, language='es', quality=1.0),
    Lang(locale=None, language='en', quality=1.0),
    Lang(locale='es_MX', language='es', quality=0.8),
]
```

Specify a default quality value:

```python
>>> parse_accept_language('en-US', default_quality=0.5)
[
    Lang(locale='en_US', language='en', quality=0.5),
]
```
