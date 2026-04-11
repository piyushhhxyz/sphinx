import abc


class Foo:
    """docstring"""

    @classmethod
    @property
    def classmethod_prop(cls) -> int:
        """docstring"""
        return 42

    @classmethod
    @property
    @abc.abstractmethod
    def classmethod_prop_abstract(cls) -> int:
        """docstring"""
        return 42


class Bar(Foo):
    """docstring"""
    pass
