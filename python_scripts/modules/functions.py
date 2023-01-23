"""This module contains functions that can be used in the template engine."""

from typing import Any


class Function:
    """Function class."""

    def __init__(self, name: str, f: callable):
        """Create a new Function instance."""
        self._name = name
        self._f = f

    def __call__(self, *args) -> Any:
        """Call the function."""
        return self._f(*args)

    def __repr__(self) -> str:
        """Return a string representation of the function."""
        return f"{self.__class__.__name__}({self._name})"


class lower(Function):
    """String lower function."""

    def __init__(self):
        """Create a new lower instance."""
        super().__init__("lower", lambda s: s.lower())


class upper(Function):
    """String upper function."""

    def __init__(self):
        """Create a new upper instance."""
        super().__init__("upper", lambda s: s.upper())


class escape_html(Function):
    """String escape function."""

    def __init__(self):
        """Create a new escape_html instance."""
        super().__init__(
            "escape", lambda s: s.replace("<", "&lt;").replace(">", "&gt;")
        )


class as_string(Function):
    """String as_string function."""

    def __init__(self):
        """Create a new as_string instance."""
        super().__init__("as_string", lambda s: str(s))
