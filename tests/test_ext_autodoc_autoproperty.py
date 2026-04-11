"""
    test_ext_autodoc_autoproperty
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test the autodoc extension.  This tests mainly the Documenters; the auto
    directives are tested in a test source file translated by test_build.

    :copyright: Copyright 2007-2021 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys

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


@pytest.mark.skipif(sys.version_info < (3, 9),
                    reason='classmethod-property requires python3.9+')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_property.Foo.classmethod_prop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.classmethod_prop',
        '   :module: target.classmethod_property',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 9),
                    reason='classmethod-property requires python3.9+')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_abstract(app):
    actual = do_autodoc(app, 'property', 'target.classmethod_property.Foo.classmethod_prop_abstract')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.classmethod_prop_abstract',
        '   :module: target.classmethod_property',
        '   :abstractmethod:',
        '   :classmethod:',
        '   :type: int',
        '',
        '   docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 9),
                    reason='classmethod-property requires python3.9+')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_autoclass(app):
    """Test that classmethod properties are documented when using autoclass."""
    options = {"members": None}
    actual = do_autodoc(app, 'class', 'target.classmethod_property.Foo', options)
    assert list(actual) == [
        '',
        '.. py:class:: Foo()',
        '   :module: target.classmethod_property',
        '',
        '   docstring',
        '',
        '',
        '   .. py:property:: Foo.classmethod_prop',
        '      :module: target.classmethod_property',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
        '',
        '   .. py:property:: Foo.classmethod_prop_abstract',
        '      :module: target.classmethod_property',
        '      :abstractmethod:',
        '      :classmethod:',
        '      :type: int',
        '',
        '      docstring',
        '',
    ]


@pytest.mark.skipif(sys.version_info < (3, 9),
                    reason='classmethod-property requires python3.9+')
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_classmethod_property_inherited(app):
    """Test that inherited classmethod properties are documented."""
    options = {"members": None, "inherited-members": None}
    actual = do_autodoc(app, 'class', 'target.classmethod_property.Bar', options)
    assert '   .. py:property:: Bar.classmethod_prop' in actual
    assert '      :classmethod:' in actual
