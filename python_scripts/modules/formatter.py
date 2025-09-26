"""Format HTML."""

from lxml.html import fromstring, tostring


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
        root = fromstring(html_text)
        return tostring(root, pretty_print=True, encoding="unicode").strip()
