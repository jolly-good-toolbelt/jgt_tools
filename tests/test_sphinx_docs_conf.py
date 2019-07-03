"""Tests for sphinx_docs/conf.py."""
import pytest

import sphinx_docs.conf

OWNER_NAME_LIST = [
    (
        "git@github.com:jolly-good-toolbelt/jgt_tools.git",
        "jolly-good-toolbelt/jgt_tools",
    ),
    (
        "https://github.com/jolly-good-toolbelt/jgt_tools.git",
        "jolly-good-toolbelt/jgt_tools",
    ),
    (
        "git@github.com:jolly.good.toolbelt/jgt_tools.git",
        "jolly.good.toolbelt/jgt_tools",
    ),
    (
        "https://github.com/jolly.good.toolbelt/jgt_tools.git",
        "jolly.good.toolbelt/jgt_tools",
    ),
]


@pytest.mark.parametrize("origin_url,owner_name", OWNER_NAME_LIST)
def test_owner_name_from(origin_url, owner_name):
    assert sphinx_docs.conf._owner_name_from(origin_url) == owner_name
