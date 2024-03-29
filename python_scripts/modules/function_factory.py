"""Function factory module."""

from __future__ import annotations

from modules.functions import Function, as_string, escape_html, lower, strip, upper


class FunctionFactory:
    """Function factory class."""

    @staticmethod
    def create(name: str) -> Function:
        """Create a function.

        Args:
            name (str): Function name

        Returns:
            Function: Function instance
        """
        functions_map = {
            "lower": lower,
            "upper": upper,
            "escape": escape_html,
            "as_string": as_string,
            "strip": strip,
        }

        if name in functions_map:
            return functions_map[name]()

        raise ValueError(f"Function {name} not found")
