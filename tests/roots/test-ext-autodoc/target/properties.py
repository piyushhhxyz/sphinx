import sys
from abc import abstractmethod


class Foo:
    """docstring"""

    @property
    def prop(self) -> int:
        """docstring"""

    if sys.version_info >= (3, 9):
        @classmethod
        @property
        def classprop(cls) -> int:
            """class property docstring"""

        @classmethod
        @property
        @abstractmethod
        def abstract_classprop(cls) -> int:
            """abstract class property docstring"""


if sys.version_info >= (3, 9):
    class SubFoo(Foo):
        """subclass docstring"""
