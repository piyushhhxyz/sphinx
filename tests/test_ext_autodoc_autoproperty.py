"""
    test_ext_autodoc_autoproperty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly the Documenters; the auto
    directives are tested in a test source file translated by test_build.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from .test_ext_autodoc import do_autodoc


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.prop',
        '   :module: target.properties',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_class_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.class_prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.class_prop',
        '   :module: target.properties',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]
