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

needs_py39 = pytest.mark.skipif(sys.version_info < (3, 9),
                                reason='classmethod+property requires Python 3.9+')


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


@needs_py39
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_class_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.classprop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.classprop',
        '   :module: target.properties',
        '   :classmethod:',
        '   :type: int',
        '',
        '   class property docstring',
        '',
    ]


@needs_py39
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_abstract_class_properties(app):
    actual = do_autodoc(app, 'property', 'target.properties.Foo.abstract_classprop')
    assert list(actual) == [
        '',
        '.. py:property:: Foo.abstract_classprop',
        '   :module: target.properties',
        '   :classmethod:',
        '   :abstractmethod:',
        '   :type: int',
        '',
        '   abstract class property docstring',
        '',
    ]


@needs_py39
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_inherited_class_properties(app):
    """Inherited @classmethod @property should be documented on the subclass."""
    actual = do_autodoc(app, 'property', 'target.properties.SubFoo.classprop')
    assert list(actual) == [
        '',
        '.. py:property:: SubFoo.classprop',
        '   :module: target.properties',
        '   :classmethod:',
        '   :type: int',
        '',
        '   class property docstring',
        '',
    ]


@needs_py39
@pytest.mark.sphinx('html', testroot='ext-autodoc')
def test_autoclass_includes_class_properties(app):
    """autoclass with :members: must include @classmethod @property members.

    Regression test: filter_members was discarding classmethod+property members
    because getdoc() returned the C-level classmethod builtin docstring instead
    of the user-defined property docstring, causing has_doc to be False.
    """
    actual = do_autodoc(app, 'class', 'target.properties.Foo', options={'members': None})
    actual_list = list(actual)
    assert any('classprop' in line for line in actual_list), (
        "classprop not found in autoclass output. "
        "classmethod+property members are being silently dropped by filter_members.\n"
        "Full output:\n" + '\n'.join(actual_list)
    )
    assert any(':classmethod:' in line for line in actual_list), (
        ":classmethod: option missing from autoclass output.\n"
        "Full output:\n" + '\n'.join(actual_list)
    )
    assert any('abstract_classprop' in line for line in actual_list), (
        "abstract_classprop not found in autoclass output.\n"
        "Full output:\n" + '\n'.join(actual_list)
    )
    assert any(':abstractmethod:' in line for line in actual_list), (
        ":abstractmethod: option missing for abstract classmethod+property.\n"
        "Full output:\n" + '\n'.join(actual_list)
    )
