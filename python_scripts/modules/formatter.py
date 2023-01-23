"""Format HTML."""
from yattag import indent


class HTMLFormatter:
    """Format HTML."""

    @classmethod
    def format(cls, html_text: str) -> str:
        """Format the HTML code.

        Args:
            html (str): The HTML to format.

        Returns:
            str: Formatted HTML.
        """
        ...
        return indent(html_text)
