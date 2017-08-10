import pytest

from accept_language import Lang, parse_accept_language, MAX_HEADER_LEN


@pytest.mark.parametrize('header_string, exp_result', [
    ('en-US', [Lang(locale='en_US', language='en', quality=1.0)]),
    ('es', [Lang(locale=None, language='es', quality=1.0)]),
    (
        'es-mx;q=0.8,es,en',
        [
            Lang(locale=None, language='es', quality=1.0),
            Lang(locale=None, language='en', quality=1.0),
            Lang(locale='es_MX', language='es', quality=0.8),
        ]
    ),
    (
        'en-US,el-GR,fr',
        [
            Lang(locale='en_US', language='en', quality=1.0),
            Lang(locale='el_GR', language='el', quality=1.0),
            Lang(locale=None, language='fr', quality=1.0),
        ]
    ),
    (
        'en-US,el;q=0.8',
        [
            Lang(locale='en_US', language='en', quality=1.0),
            Lang(locale=None, language='el', quality=0.8),
        ]
    ),
    # ignores whitespace
    (
        'en-US,  el-gr ,    fr ',
        [
            Lang(locale='en_US', language='en', quality=1.0),
            Lang(locale='el_GR', language='el', quality=1.0),
            Lang(locale=None, language='fr', quality=1.0),
        ]
    ),
    # ignores case
    (
        'en-us,EL-gr,FR',
        [
            Lang(locale='en_US', language='en', quality=1.0),
            Lang(locale='el_GR', language='el', quality=1.0),
            Lang(locale=None, language='fr', quality=1.0),
        ]
    ),
    # skips parts with invalid formatting
    (
        'el,-us,en-,12-34,en-US:q=0,fr',
        [
            Lang(locale=None, language='el', quality=1.0),
            Lang(locale=None, language='fr', quality=1.0),
        ]
    ),
    # wildcard is ignored
    (
        'en-GB,*;q=0.5', [Lang(locale='en_GB', language='en', quality=1.0)]
    ),
])
def test_parses_header_value(header_string, exp_result):
    parsed = parse_accept_language(header_string)
    assert exp_result == parsed


def test_sorts_results_by_quality_descending():
    parsed = parse_accept_language('en-US;q=0.8,el;q=1.0')
    expected = [
        Lang(locale=None, language='el', quality=1.0),
        Lang(locale='en_US', language='en', quality=0.8),
    ]
    assert expected == parsed


def test_validates_header_length():
    with pytest.raises(ValueError) as exc:
        parse_accept_language('x' * (MAX_HEADER_LEN + 1))
    exc.match(r'Accept-Language too long, max length is 8192')
