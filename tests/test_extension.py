"""Tests for sphinx.extension module."""

import pytest
from unittest.mock import MagicMock

from sphinx.extension import Extension, verify_needs_extensions
from sphinx.errors import VersionRequirementError


def test_verify_needs_extensions_version_comparison():
    """Regression test: version comparison must use semantic versioning,
    not string comparison.  Previously '0.10.0' was rejected when '0.6.0'
    was required because '0.6' > '0.10' lexicographically."""
    app = MagicMock()
    app.extensions = {
        'some_ext': Extension('some_ext', None, version='0.10.0'),
    }
    config = MagicMock()
    config.needs_extensions = {'some_ext': '0.6.0'}

    # Should NOT raise: 0.10.0 >= 0.6.0
    verify_needs_extensions(app, config)


def test_verify_needs_extensions_reject_older():
    """Ensure an older loaded version is still correctly rejected."""
    app = MagicMock()
    app.extensions = {
        'some_ext': Extension('some_ext', None, version='0.5.0'),
    }
    config = MagicMock()
    config.needs_extensions = {'some_ext': '0.6.0'}

    with pytest.raises(VersionRequirementError):
        verify_needs_extensions(app, config)


def test_verify_needs_extensions_accept_equal():
    """Exact version match should be accepted."""
    app = MagicMock()
    app.extensions = {
        'some_ext': Extension('some_ext', None, version='0.6.0'),
    }
    config = MagicMock()
    config.needs_extensions = {'some_ext': '0.6.0'}

    verify_needs_extensions(app, config)


def test_verify_needs_extensions_unknown_version():
    """Extensions with 'unknown version' should be rejected."""
    app = MagicMock()
    app.extensions = {
        'some_ext': Extension('some_ext', None),
    }
    config = MagicMock()
    config.needs_extensions = {'some_ext': '0.6.0'}

    with pytest.raises(VersionRequirementError):
        verify_needs_extensions(app, config)


def test_verify_needs_extensions_missing_extension():
    """Missing extensions should produce a warning, not an error."""
    app = MagicMock()
    app.extensions = {}
    config = MagicMock()
    config.needs_extensions = {'missing_ext': '0.1'}

    # Should not raise, just warn
    verify_needs_extensions(app, config)
