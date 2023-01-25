"""Format HTML."""


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
        raise NotImplementedError("Formatter has not been implemented yet")
