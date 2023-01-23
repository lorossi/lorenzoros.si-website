from lxml import etree, html


class HTMLFormatter:
    @classmethod
    def format(cls, html_text: str) -> str:
        """Format the HTML.

        Args:
            html (str): The HTML to format.

        Returns:
            str: Formatted HTML.
        """
        document_root = html.fromstring(html_text)
        return etree.tostring(document_root, encoding="unicode", pretty_print=True)
